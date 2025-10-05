import numpy as np
from scipy.stats import norm
import pandas as pd
from typing import Literal, Optional
from .generate_synthetic import wylicz_emeryture, load_parameters

class EmeryturaModel:
    def __init__(self, param_csv_path, dataset, std=1.0, noise_lvl=0.02):
        self.df = load_parameters(param_csv_path)
        self.std = std  # Standard deviation for log_prob
        self.dataset = dataset

    def predict_log_prob(self, X, y_key="emerytura_nominalna"):
        """
        X: list of dicts or pandas DataFrame with keys/columns:
            plec, wynagrodzenie_brutto, rok_rozpoczecia, rok_zakonczenia, suma_wplaconych_skladek, kapital_poczatkowy (optional)
        y_key: which output to compare (default: emerytura_nominalna)
        Returns: np.array of log probabilities
        """
        if isinstance(X, pd.DataFrame):
            X = X.to_dict(orient="records")
        log_probs = []
        for row in X:
            X_unnormalized = self.dataset.destandardize_train(row)
            wynik = wylicz_emeryture(
                self.df,
                X_unnormalized[-1], 
                X_unnormalized[:-1]
            )
            y_true = X_unnormalized[y_key]
            y_pred = wynik[y_key]
            log_prob = norm(loc=y_pred, scale=self.std).logpdf(y_true)
            log_probs.append(log_prob)
        return np.array(log_probs)
