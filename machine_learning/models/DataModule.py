import torch
import pandas as pd
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import pytorch_lightning as pl

class CSVDataset(Dataset):
    """Dataset do wczytywania danych z CSV"""
    def __init__(self, X, y):
        self.X = torch.FloatTensor(X)
        self.y = torch.FloatTensor(y)
    
    def __len__(self):
        return len(self.X)
    
    def __getitem__(self, idx):
        return self.X[idx], (self.y[idx] > torch.randint(5_000, 7_500, size=(1, ))).float().squeeze()


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
    def __init__(self, csv_path, target_column,  
                 categorical_columns=["plec"], 
                 numerical_columns=["wynagrodzenie_brutto","rok_rozpoczecia","rok_zakonczenia","suma_wplaconych_skladek",], 
                 batch_size=32, 
                 test_size=0.2, 
                 val_size=0.1, 
                 random_state=42):
        super().__init__()
        self.csv_path = csv_path
        self.target_column = target_column
        self.categorical_columns = categorical_columns or []
        self.numerical_columns = numerical_columns or []
        print("CCC>>>", self.categorical_columns, self.numerical_columns)
        self.batch_size = batch_size
        self.test_size = test_size
        self.val_size = val_size
        self.random_state = random_state
        self.preprocessor = ColumnPreprocessor(categorical_columns, numerical_columns)
        self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None

    def setup(self, stage=None):
        df = pd.read_csv(self.csv_path)
        print(">>> Loaded data columns:", df.columns)

        X = df.drop(columns=[self.target_column])
        y = df[self.target_column].values
        
        X_temp, X_test, y_temp, y_test = train_test_split(
            X, y, test_size=self.test_size, random_state=self.random_state
        )
        
        val_ratio = self.val_size / (1 - self.test_size)
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp, test_size=val_ratio, random_state=self.random_state
        )
        
        self.X_train = self.preprocessor.fit_transform(X_train)
        self.X_val = self.preprocessor.transform(X_val)
        self.X_test = self.preprocessor.transform(X_test)
        
        self.train_dataset = CSVDataset(self.X_train, y_train)
        self.val_dataset = CSVDataset(self.X_val, y_val)
        self.test_dataset = CSVDataset(self.X_test, y_test)

        self.y_train = torch.concat([self.train_dataset[i][1].unsqueeze(0) for i in range(len(self.train_dataset))])
        self.y_val = torch.concat([self.val_dataset[i][1].unsqueeze(0) for i in range(len(self.val_dataset))])
        self.y_test = torch.concat([self.test_dataset[i][1].unsqueeze(0) for i in range(len(self.test_dataset))])
        
        self.input_dim = self.X_train.shape[1]

    def get_cv_splits(self, n_splits=5):
        kf = KFold(n_splits=n_splits, shuffle=True, random_state=self.random_state)
        for train_index, val_index in kf.split(self.X_train):
            X_tr, X_val = self.X_train[train_index], self.X_train[val_index]
            y_tr, y_val = self.y_train[train_index], self.y_train[val_index]
            yield CSVDataset(X_tr, y_tr), CSVDataset(X_val, y_val)
    
    def train_dataloader(self):
        return DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=True, num_workers=4)
    
    def val_dataloader(self):
        return DataLoader(self.val_dataset, batch_size=self.batch_size, num_workers=4)
    
    def test_dataloader(self):
        return DataLoader(self.test_dataset, batch_size=self.batch_size, num_workers=4)

    def destandardize_train(self, X):
        return self.preprocessor.inverse_transform(X)

    def destandardize_test(self, X):
        return self.preprocessor.inverse_transform(X)