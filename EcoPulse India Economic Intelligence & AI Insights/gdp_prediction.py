"""
EcoPulse India Economic Intelligence
GDP Prediction - Regression Models (Improved)
"""

import pandas as pd
import numpy as np
import os
import sys
import joblib
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from helpers import setup_logging, load_data

logger = setup_logging()


class GDPPredictor:
    """Regression models with improved features."""

    def __init__(self):
        self.scaler = StandardScaler()
        self.models = {}
        self.results = {}

    def prepare_data(self, df):
        """Prepare with all available numeric features."""
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

    def train_models(self, X_train, X_test, y_train, y_test):
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        models = {
            'Linear Regression': LinearRegression(),
            'Random Forest': RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42),
            'Gradient Boosting': GradientBoostingRegressor(n_estimators=200, max_depth=5, random_state=42)
        }

        for name, model in models.items():
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)

            self.models[name] = model
            self.results[name] = {
                'MAE': mean_absolute_error(y_test, y_pred),
                'RMSE': np.sqrt(mean_squared_error(y_test, y_pred)),
                'R2': r2_score(y_test, y_pred)
            }
            logger.info(f"{name} - R2: {self.results[name]['R2']:.4f}")

        return self.results

    def save_best_model(self):
        best_name = max(self.results, key=lambda k: self.results[k]['R2'])
        os.makedirs('models', exist_ok=True)
        joblib.dump(self.models[best_name], 'models/gdp_model.pkl')
        joblib.dump(self.scaler, 'models/gdp_scaler.pkl')
        logger.info(f"Best model saved: {best_name}")
        return best_name


def run_gdp_prediction():
    df = load_data('ecopulse_processed.csv')
    if df is None:
        logger.error("Processed data not found")
        return

    predictor = GDPPredictor()
    X_train, X_test, y_train, y_test = predictor.prepare_data(df)
    results = predictor.train_models(X_train, X_test, y_train, y_test)

    print("\n" + "=" * 60)
    print("GDP PREDICTION RESULTS")
    print("=" * 60)
    for model, metrics in results.items():
        print(f"\n{model}:")
        for k, v in metrics.items():
            print(f"  {k}: {v:.4f}")

    predictor.save_best_model()
    return results


if __name__ == "__main__":
    run_gdp_prediction()