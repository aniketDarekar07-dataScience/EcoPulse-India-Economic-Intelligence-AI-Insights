"""
EcoPulse India Economic Intelligence
XGBoost and LightGBM Models
"""

import pandas as pd
import numpy as np
import os
import sys
import joblib
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import xgboost as xgb
import lightgbm as lgb

from helpers import setup_logging, load_data

logger = setup_logging()


class BoostingModels:
    """Gradient boosting models for GDP prediction."""

    def __init__(self):
        self.models = {}
        self.results = {}

    def prepare_data(self, df):
        feature_cols = [
            'Year', 'Quarter_Number', 'Employment', 'Exports', 'Imports',
            'FDI', 'Inflation', 'CPI', 'IIP', 'Tax_Revenue',
            'Trade_Balance', 'GDP_per_Employment', 'Trade_Openness',
            'FDI_to_GDP', 'Tax_Efficiency'
        ]

        available = [c for c in feature_cols if c in df.columns]
        X = df[available].fillna(df[available].median())
        y = df['GDP'].fillna(df['GDP'].median())

        return train_test_split(X, y, test_size=0.2, random_state=42)

    def train_all(self, X_train, X_test, y_train, y_test):
        xgb_model = xgb.XGBRegressor(
            n_estimators=200, learning_rate=0.05, max_depth=6,
            random_state=42, verbosity=0
        )
        xgb_model.fit(X_train, y_train)
        y_pred = xgb_model.predict(X_test)

        self.models['XGBoost'] = xgb_model
        self.results['XGBoost'] = {
            'MAE': mean_absolute_error(y_test, y_pred),
            'RMSE': np.sqrt(mean_squared_error(y_test, y_pred)),
            'R2': r2_score(y_test, y_pred)
        }
        logger.info(f"XGBoost R2: {self.results['XGBoost']['R2']:.4f}")

        lgb_model = lgb.LGBMRegressor(
            n_estimators=200, learning_rate=0.05, max_depth=6,
            random_state=42, verbose=-1
        )
        lgb_model.fit(X_train, y_train)
        y_pred = lgb_model.predict(X_test)

        self.models['LightGBM'] = lgb_model
        self.results['LightGBM'] = {
            'MAE': mean_absolute_error(y_test, y_pred),
            'RMSE': np.sqrt(mean_squared_error(y_test, y_pred)),
            'R2': r2_score(y_test, y_pred)
        }
        logger.info(f"LightGBM R2: {self.results['LightGBM']['R2']:.4f}")

        return self.results

    def save_best(self):
        best_name = max(self.results, key=lambda k: self.results[k]['R2'])
        os.makedirs('models', exist_ok=True)
        joblib.dump(self.models[best_name], 'models/xgboost_model.pkl')
        logger.info(f"Best boosting model saved: {best_name}")
        return best_name


def run_xgboost():
    df = load_data('ecopulse_processed.csv')
    if df is None:
        logger.error("Processed data not found")
        return

    models = BoostingModels()
    X_train, X_test, y_train, y_test = models.prepare_data(df)
    results = models.train_all(X_train, X_test, y_train, y_test)

    print("\n" + "=" * 60)
    print("BOOSTING MODELS RESULTS")
    print("=" * 60)
    for name, metrics in results.items():
        print(f"\n{name}:")
        for k, v in metrics.items():
            print(f"  {k}: {v:.4f}")

    models.save_best()
    return results


if __name__ == "__main__":
    run_xgboost()