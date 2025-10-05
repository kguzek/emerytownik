from .base import AbstractDataset
import pandas as pd
import torch
from torch.utils.data import DataLoader, Dataset
from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import pytorch_lightning as pl
import numpy as np
import pickle


class DataModule(AbstractDataset):
    def __init__(self, csv_path, target_column,random_state=42,save_preprocessing_module=True,preprocessing_module_path=None, test_path=None
                 ):
        super().__init__()
        self.target_column = target_column
        self.random_state = random_state
        self.categorical_columns=["plec"]#  or []
        self.numerical_columns=["wynagrodzenie_brutto","rok_rozpoczecia","rok_zakonczenia","suma_wplaconych_skladek"]#  or []
        self.csv_path = csv_path
        self.raw_data = pd.read_csv(csv_path)
        self.X, self.y = self.preprocess(raw_data=self.raw_data)
        self.X_train, self.X_test, self.y_train, self.y_test = self.get_split_data(
            self.X, self.y
        )
        print("Train shape >>>", self.X_train.shape, self.y_train.shape, self.X_train.columns)
        print("Test shape >>>", self.X_test.shape, self.y_test.shape, self.X_test.columns)
        self.X_train, self.X_test, self.y_train, self.y_test = self.transform(
            self.X_train, self.X_test, self.y_train, self.y_test
        )
        print("Test shape >>>", self.X_test.shape, self.y_test.shape)
        if save_preprocessing_module:
            with open(preprocessing_module_path, "wb") as f:
                pickle.dump(self, f)
                print("Preprocessing module saved to data_module_preprocessing.pkl")

    @staticmethod
    def load_from_pickle(path="./checkpoints/data_module_preprocessing.pkl"):
        with open(path, "rb") as f:
            return pickle.load(f)

    def read_new_test(self, path):
        new_raw_data = pd.read_csv(path)
        X_new, y_new = self.preprocess(raw_data=new_raw_data)
        X_new_transformed = self.feature_transformer.transform(X_new)
        X_new_transformed = X_new_transformed.astype(np.float32)
        y_new = y_new.astype(np.int64)
        return X_new_transformed, y_new

    def preprocess(self, raw_data: pd.DataFrame):
        """
        Preprocess the loaded data to X and y numpy arrays.
        """
        self.feature_columns = [*self.categorical_columns, *self.numerical_columns]
        print("Feature columns >>>", self.feature_columns)
        X = raw_data[self.feature_columns]
        X['plec'] = X['plec'].map({'m':0,'k':1})
        y = raw_data[self.target_column].to_numpy() 
    
        return X, y

    def destandardize_train(self, row):
        X_unnormalized = {}
        for i, col in enumerate(self.feature_columns):
            if col in self.numerical_columns:
                mean = self.feature_transformer.named_transformers_['StandardScaler'].mean_[self.numerical_columns.index(col)]
                scale = np.sqrt(self.feature_transformer.named_transformers_['StandardScaler'].var_[self.numerical_columns.index(col)])
                X_unnormalized[col] = row[i].item() * scale + mean
            else:
                X_unnormalized[col] = {0:'m',1:'k'}.get(int(row[i].item()), row[i].item())
        return X_unnormalized
    
    def destandardize_train_batch(self, X_batch):
        """
        Destandardize a batch of training data.
        X_batch: torch.Tensor of shape (batch_size, num_features) or numpy array
        Returns: list of dictionaries with destandardized values
        """
        if isinstance(X_batch, np.ndarray):
            X_batch = torch.from_numpy(X_batch)
        
        # Handle single row case
        if len(X_batch.shape) == 1:
            return [self.destandardize_train(X_batch)]
        
        # Process each row in the batch
        results = []
        for i in range(X_batch.shape[0]):
            row = X_batch[i]
            X_unnormalized = self.destandardize_train(row)
            results.append(X_unnormalized)
        
        return results

    def transform(
        self,
        X_train: np.ndarray,
        X_test: np.ndarray,
        y_train: np.ndarray,
        y_test: np.ndarray,
    ):
        """
        Transform the loaded data by applying Min-Max scaling to the features.
        """
        self.feature_transformer = ColumnTransformer(
            [
                ("StandardScaler", StandardScaler(), self.numerical_columns),
            ],
            remainder="passthrough",
        )
        # self.feature_transformer.set_output(transform='pandas')
        print("Before transform train >>>", X_train[:1])
        print("Before transform test >>>", X_train[:1])
        X_train = self.feature_transformer.fit_transform(X_train)
        X_test = self.feature_transformer.transform(X_test)
        
        print("After transform train >>>", X_train[:1])
        print("After transform test >>>", X_train[:1])

        X_train = X_train.astype(np.float32)
        X_test = X_test.astype(np.float32)
        y_train = y_train.astype(np.int64)
        y_test = y_test.astype(np.int64)

        self.numerical_features = list(range(0, len(self.numerical_columns)))
        self.categorical_features = list(
            range(len(self.numerical_columns), X_train.shape[1])
        )
        self.actionable_features = list(range(0, X_train.shape[1]))  # [1:-1]

        return X_train, X_test, y_train, y_test