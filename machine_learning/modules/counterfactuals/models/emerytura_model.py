import numpy as np
from scipy.stats import norm
import pandas as pd
from typing import Literal, Optional, Union
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from data.generate_synthetic import wylicz_emeryture, load_parameters
import pickle


class EmeryturaModel(nn.Module):
    def __init__(self, param_csv_path, dataset, std=1.0, train_model=False, noise_lvl=0.02, batch_size=None, seed=42, pretrained_path=None):
        super().__init__()
        self.df = load_parameters(param_csv_path)
        self.std = std  # Standard deviation for log_prob
        self.dataset = dataset
        
        # Store feature statistics for Naive Bayes
        self.feature_means = {}
        self.feature_stds = {}
        self.class_prior = None
        self.naive_bayes = None 
        self.pretrained_path = pretrained_path
        np.random.seed(seed)

    def save(self):
        with open(self.pretrained_path, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(path="./checkpoints/emerytura_model.pkl"):
        with open(path, "rb") as f:
            model = pickle.load(f)
        return model
        
    def forward(self, X, context=None):
        """
        Forward pass through the model.
        X: torch.Tensor of shape (batch_size, num_features) with normalized features
        Returns: torch.Tensor of predictions
        """
        predictions = []
        
        # Process each sample in the batch
        for i in range(X.shape[0]):
            # Convert tensor row to dict format for destandardization
            row = X[i]
            
            # Denormalize the input features
            X_unnormalized = self.dataset.destandardize_train(row)
            
            # Use wylicz_emeryture to compute the prediction
            wynik = wylicz_emeryture(
                self.df,
                X_unnormalized['plec'],
                X_unnormalized['wynagrodzenie_brutto'],
                int(X_unnormalized['rok_rozpoczecia']),
                int(X_unnormalized['rok_zakonczenia']),
                X_unnormalized['suma_wplaconych_skladek'],
                X_unnormalized.get('kapital_poczatkowy', 0),  # Use 0 as default if not present
                dzielnik_csv_path="./data/Parametry-III 2025 - e_x M i K-PROGNOZA.csv"
            )

             # Extract the nominal pension
            prediction = wynik['emerytura_nominalna']
            
            # Extract the nominal pension (or whatever output you need)
            threshold = np.random.randint(5000, 7_500)
            bool_prediction = prediction > threshold
            predictions.append(bool_prediction)
    
        # Convert to tensor and return
        return torch.tensor(predictions, dtype=torch.bool)

    def fit_naive_bayes(self, X_train):
        """
        Fit Naive Bayes by computing feature statistics from training data.
        X_train: DataLoader, list of dicts, or pandas DataFrame
        """
        # Collect all features
        all_features = []
        
        if isinstance(X_train, DataLoader):
            for batch in X_train:
                batch_row, _ = batch
                for row in batch_row:
                    X_unnormalized = self.dataset.destandardize_train(row)
                    all_features.append(X_unnormalized)
        elif isinstance(X_train, pd.DataFrame):
            all_features = X_train.to_dict(orient="records")
        else:
            all_features = X_train
            
        # Convert to DataFrame for easier statistics computation
        df_features = pd.DataFrame(all_features)
        
        # Compute mean and std for each numerical feature
        numerical_cols = df_features.select_dtypes(include=[np.number]).columns
        for col in numerical_cols:
            self.feature_means[col] = df_features[col].mean()
            self.feature_stds[col] = df_features[col].std() + 1e-10  # Add small epsilon to avoid division by zero
            
        # For categorical features (like 'plec'), compute frequencies
        categorical_cols = df_features.select_dtypes(exclude=[np.number]).columns
        for col in categorical_cols:
            self.feature_means[col] = df_features[col].value_counts(normalize=True).to_dict()
    
    def _compute_feature_log_prob(self, feature_name, feature_value):
        """
        Compute log probability of a feature value using Gaussian assumption for numerical
        and frequency for categorical features.
        """
        if feature_name in self.feature_stds:
            # Numerical feature - use Gaussian
            mean = self.feature_means[feature_name]
            std = self.feature_stds[feature_name]
            log_prob = norm(loc=mean, scale=std).logpdf(feature_value)
        elif feature_name in self.feature_means and isinstance(self.feature_means[feature_name], dict):
            # Categorical feature - use frequency
            freq_dict = self.feature_means[feature_name]
            prob = freq_dict.get(feature_value, 1e-10)  # Small probability for unseen values
            log_prob = np.log(prob)
        else:
            # Unknown feature - assign uniform log probability
            log_prob = 0.0
            
        return log_prob

    def predict_log_prob(self, X, y_key="emerytura_nominalna"):
        """
        X: DataLoader, list of dicts, or pandas DataFrame with keys/columns:
            plec, wynagrodzenie_brutto, rok_rozpoczecia, rok_zakonczenia, suma_wplaconych_skladek, kapital_poczatkowy (optional)
        y_key: which output to compare (default: emerytura_nominalna)
        Returns: np.array of log probabilities using Naive Bayes
        """
        log_probs = []
        
        # Define features to use for Naive Bayes (excluding the target)
        feature_keys = ['plec', 'wynagrodzenie_brutto', 'rok_rozpoczecia', 
                       'rok_zakonczenia', 'suma_wplaconych_skladek']
        
        if isinstance(X, DataLoader):
            with torch.no_grad():
                for batch in X:
                    batch_row, _ = batch
                    for row in batch_row:
                        X_unnormalized = self.dataset.destandardize_train_batch(row)
                        
                        # Compute Naive Bayes log probability
                        # P(x1, x2, ..., xn) = P(x1) * P(x2) * ... * P(xn)
                        # log P(x1, x2, ..., xn) = log P(x1) + log P(x2) + ... + log P(xn)
                        log_prob = 0.0
                        for feature_key in feature_keys:
                            if feature_key in X_unnormalized:
                                feature_value = X_unnormalized[feature_key]
                                log_prob += self._compute_feature_log_prob(feature_key, feature_value)
                        
                        log_probs.append(log_prob)
        else:
            if isinstance(X, pd.DataFrame):
                X = X.to_dict(orient="records")
            for row in X:
                X_unnormalized = self.dataset.destandardize_train_batch(row)
                
                # Compute Naive Bayes log probability
                log_prob = 0.0
                for feature_key in feature_keys:
                    if feature_key in X_unnormalized:
                        feature_value = X_unnormalized[feature_key]
                        log_prob += self._compute_feature_log_prob(feature_key, feature_value)
                
                log_probs.append(log_prob)
                
        return torch.from_numpy(np.array(log_probs))