import argparse
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score
import numpy as np


class CSVDataset(Dataset):
    """Dataset do wczytywania danych z CSV"""
    def __init__(self, X, y):
        self.X = torch.FloatTensor(X)
        self.y = torch.FloatTensor(y)
    
    def __len__(self):
        return len(self.X)
    
    def __getitem__(self, idx):
        return self.X[idx], (self.y[idx] > torch.randint(5_000, 7_500, size=(1, ))).float().squeeze()


class MLPClassifier(pl.LightningModule):
    def __init__(self, input_dim, hidden_dims, learning_rate=0.001, dropout=0.2):
        super().__init__()
        self.save_hyperparameters()
        self.learning_rate = learning_rate
        
        layers = []
        prev_dim = input_dim
        
        for hidden_dim in hidden_dims:
            layers.append(nn.Linear(prev_dim, hidden_dim))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout))
            prev_dim = hidden_dim
        
        layers.append(nn.Linear(prev_dim, 1))
        layers.append(nn.Sigmoid())
        
        self.model = nn.Sequential(*layers)
        self.criterion = nn.BCELoss()
        
        self.validation_step_outputs = []
        self.test_step_outputs = []
    
    def forward(self, x):
        return self.model(x)
    
    def predict_log_prob(self, x):
        self.eval()
        with torch.no_grad():
            probs = self(x).squeeze()
            log_probs = torch.log(probs + 1e-10)
            return log_probs
    
    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x).squeeze()
        loss = self.criterion(y_hat, y)
        
        preds = (y_hat > 0.5).float()
        acc = (preds == y).float().mean()
        
        self.log('train_loss', loss, prog_bar=True)
        self.log('train_acc', acc, prog_bar=True)
        return loss
    
    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x).squeeze()
        loss = self.criterion(y_hat, y)
        
        self.validation_step_outputs.append({
            'loss': loss,
            'preds': y_hat,
            'targets': y
        })
        
        return loss
    
    def on_validation_epoch_end(self):
        all_preds = torch.cat([x['preds'] for x in self.validation_step_outputs])
        all_targets = torch.cat([x['targets'] for x in self.validation_step_outputs])
        avg_loss = torch.stack([x['loss'] for x in self.validation_step_outputs]).mean()
        
        preds_binary = (all_preds > 0.5).cpu().numpy()
        targets_np = all_targets.cpu().numpy()
        
        acc = accuracy_score(targets_np, preds_binary)
        
        self.log('val_loss', avg_loss, prog_bar=True)
        self.log('val_acc', acc, prog_bar=True)
        
        self.validation_step_outputs.clear()
    
    def test_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x).squeeze()
        loss = self.criterion(y_hat, y)
        
        self.test_step_outputs.append({
            'loss': loss,
            'preds': y_hat,
            'targets': y
        })
        
        return loss
    
    def on_test_epoch_end(self):
        all_preds = torch.cat([x['preds'] for x in self.test_step_outputs])
        all_targets = torch.cat([x['targets'] for x in self.test_step_outputs])
        avg_loss = torch.stack([x['loss'] for x in self.test_step_outputs]).mean()
        
        preds_binary = (all_preds > 0.5).cpu().numpy()
        targets_np = all_targets.cpu().numpy()
        
        acc = accuracy_score(targets_np, preds_binary)
        
        print(f"\nTest Metrics:")
        print(f"Loss: {avg_loss:.4f}")
        print(f"Accuracy: {acc:.4f}")
        
        self.log('test_loss', avg_loss)
        self.log('test_acc', acc)
        
        self.test_step_outputs.clear()
    
    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=self.learning_rate)
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, mode='min', factor=0.5, patience=5, verbose=True
        )
        return {
            'optimizer': optimizer,
            'lr_scheduler': {
                'scheduler': scheduler,
                'monitor': 'val_loss'
            }
        }


class ColumnPreprocessor:
    def __init__(self, categorical_columns=None, numerical_columns=None):
        self.categorical_columns = categorical_columns or []
        self.numerical_columns = numerical_columns or []
        self.preprocessor = None
        
    def fit_transform(self, df):
        transformers = []
        
        if self.numerical_columns:
            transformers.append(
                ('num', StandardScaler(), self.numerical_columns)
            )
        
        if self.categorical_columns:
            transformers.append(
                ('cat', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'), 
                 self.categorical_columns)
            )
        
        if not transformers:
            raise ValueError("At least one of categorical_columns or numerical_columns must be provided")
        
        self.preprocessor = ColumnTransformer(
            transformers=transformers,
            remainder='drop'
        )
        
        return self.preprocessor.fit_transform(df)
    
    def transform(self, df):
        if self.preprocessor is None:
            raise ValueError("Preprocessor must be fitted first. Call fit_transform() before transform()")
        return self.preprocessor.transform(df)


class DataModule(pl.LightningDataModule):
    def __init__(self, csv_path, target_column,  categorical_columns=None, numerical_columns=None, batch_size=32, test_size=0.2, val_size=0.1, random_state=42):
        super().__init__()
        self.csv_path = csv_path
        self.target_column = target_column
        self.categorical_columns = categorical_columns or []
        self.numerical_columns = numerical_columns or []
        self.batch_size = batch_size
        self.test_size = test_size
        self.val_size = val_size
        self.random_state = random_state
        self.preprocessor = ColumnPreprocessor(categorical_columns, numerical_columns)

    def setup(self, stage=None):
        df = pd.read_csv(self.csv_path)

        X = df.drop(columns=[self.target_column])
        y = df[self.target_column].values
        
        X_temp, X_test, y_temp, y_test = train_test_split(
            X, y, test_size=self.test_size, random_state=self.random_state
        )
        
        val_ratio = self.val_size / (1 - self.test_size)
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp, test_size=val_ratio, random_state=self.random_state
        )
        
        X_train = self.preprocessor.fit_transform(X_train)
        X_val = self.preprocessor.transform(X_val)
        X_test = self.preprocessor.transform(X_test)
        
        self.train_dataset = CSVDataset(X_train, y_train)
        self.val_dataset = CSVDataset(X_val, y_val)
        self.test_dataset = CSVDataset(X_test, y_test)
        
        self.input_dim = X_train.shape[1]
    
    def train_dataloader(self):
        return DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=True, num_workers=4)
    
    def val_dataloader(self):
        return DataLoader(self.val_dataset, batch_size=self.batch_size, num_workers=4)
    
    def test_dataloader(self):
        return DataLoader(self.test_dataset, batch_size=self.batch_size, num_workers=4)


def parse_args():
    parser = argparse.ArgumentParser(description='Trening sieci MLP do klasyfikacji binarnej w PyTorch Lightning')
    
    parser.add_argument('--csv_path', type=str, required=True, help='Ścieżka do pliku CSV')
    parser.add_argument('--target_column', type=str, required=True, help='Nazwa kolumny docelowej (0/1)')
    parser.add_argument('--test_size', type=float, default=0.2, help='Rozmiar zbioru testowego')
    parser.add_argument('--val_size', type=float, default=0.1, help='Rozmiar zbioru walidacyjnego')

    parser.add_argument('--hidden_dims', type=int, nargs='+', default=[128, 64, 32], 
                        help='Rozmiary warstw ukrytych, np. --hidden_dims 128 64 32')
    parser.add_argument('--dropout', type=float, default=0.2, help='Współczynnik dropout')
    parser.add_argument('--categorical_columns', type=str, nargs='*', default=["plec"], 
                        help='Nazwy kolumn kategorycznych do one-hot encoding')
    parser.add_argument('--numerical_columns', type=str, nargs='*', default=["wynagrodzenie_brutto","rok_rozpoczecia","rok_zakonczenia","suma_wplaconych_skladek",], 
                        help='Nazwy kolumn numerycznych do standaryzacji')
    
    parser.add_argument('--batch_size', type=int, default=32, help='Rozmiar batcha')
    parser.add_argument('--learning_rate', type=float, default=0.001, help='Learning rate')
    parser.add_argument('--epochs', type=int, default=100, help='Liczba epok')
    parser.add_argument('--patience', type=int, default=10, help='Patience dla early stopping')
    
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    parser.add_argument('--accelerator', type=str, default='auto', help='Typ akceleratora (cpu, gpu, auto)')
    
    return parser.parse_args()


def main():
    args = parse_args()
    
    pl.seed_everything(args.seed)
    
    data_module = DataModule(
        csv_path=args.csv_path,
        categorical_columns=args.categorical_columns,
        numerical_columns=args.numerical_columns,
        target_column=args.target_column,
        batch_size=args.batch_size,
        test_size=args.test_size,
        val_size=args.val_size,
        random_state=args.seed
    )
    data_module.setup()
    
    model = MLPClassifier(
        input_dim=data_module.input_dim,
        hidden_dims=args.hidden_dims,
        learning_rate=args.learning_rate,
        dropout=args.dropout
    )
    
    checkpoint_callback = ModelCheckpoint(
        monitor='val_loss',
        dirpath='checkpoints',
        filename='mlp-{epoch:02d}-{val_loss:.4f}',
        save_top_k=3,
        mode='min'
    )
    
    early_stop_callback = EarlyStopping(
        monitor='val_loss',
        patience=args.patience,
        mode='min',
        verbose=True
    )
    
    trainer = pl.Trainer(
        max_epochs=args.epochs,
        accelerator=args.accelerator,
        callbacks=[checkpoint_callback, early_stop_callback],
        log_every_n_steps=10,
        enable_progress_bar=True
    )
    
    print("Rozpoczynam trening...")
    trainer.fit(model, data_module)
    
    print("\nEwaluacja na zbiorze testowym...")
    trainer.test(model, data_module)
    
    print(f"\nNajlepszy model zapisany w: {checkpoint_callback.best_model_path}")


if __name__ == '__main__':
    main()