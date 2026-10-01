"""
EcoPulse India Economic Intelligence
Growth Classification (Improved)
"""

import pandas as pd
import numpy as np
import os
import sys
import joblib
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from helpers import setup_logging, load_data

logger = setup_logging()


class GrowthClassifier:
    """Classify growth category with better features."""

    def __init__(self):
        self.scaler = StandardScaler()
        self.encoder = LabelEncoder()
        self.models = {}
        self.results = {}

    def prepare_data(self, df):
        feature_cols = [
            'Year', 'Quarter_Number', 'GDP', 'Employment', 'Exports',
            'Imports', 'FDI', 'Inflation', 'CPI', 'IIP', 'Tax_Revenue',
            'Trade_Balance', 'GDP_per_Employment', 'Trade_Openness',
            'FDI_to_GDP', 'Tax_Efficiency'
        ]

        available = [c for c in feature_cols if c in df.columns]
        X = df[available].fillna(df[available].median())
        y = df['Growth_Category'].fillna('Moderate').astype(str)

        y_enc = self.encoder.fit_transform(y)
        return train_test_split(X, y_enc, test_size=0.2, random_state=42, stratify=y_enc)

    def train_models(self, X_train, X_test, y_train, y_test):
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        models = {
            'Logistic Regression': LogisticRegression(max_iter=2000, random_state=42),
            'Random Forest': RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42),
            'Gradient Boosting': GradientBoostingClassifier(n_estimators=200, max_depth=5, random_state=42)
        }

        for name, model in models.items():
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)

            self.models[name] = model
            self.results[name] = {
                'Accuracy': accuracy_score(y_test, y_pred),
                'Precision': precision_score(y_test, y_pred, average='weighted', zero_division=0),
                'Recall': recall_score(y_test, y_pred, average='weighted', zero_division=0),
                'F1': f1_score(y_test, y_pred, average='weighted', zero_division=0)
            }
            logger.info(f"{name} - Accuracy: {self.results[name]['Accuracy']:.4f}")

        return self.results

    def save_best_model(self):
        best_name = max(self.results, key=lambda k: self.results[k]['Accuracy'])
        os.makedirs('models', exist_ok=True)
        joblib.dump(self.models[best_name], 'models/growth_classifier.pkl')
        joblib.dump(self.scaler, 'models/growth_scaler.pkl')
        joblib.dump(self.encoder, 'models/growth_encoder.pkl')
        logger.info(f"Best classifier saved: {best_name}")
        return best_name


def run_growth_classification():
    df = load_data('ecopulse_processed.csv')
    if df is None:
        logger.error("Processed data not found")
        return

    classifier = GrowthClassifier()
    X_train, X_test, y_train, y_test = classifier.prepare_data(df)
    results = classifier.train_models(X_train, X_test, y_train, y_test)

    print("\n" + "=" * 60)
    print("GROWTH CLASSIFICATION RESULTS")
    print("=" * 60)
    for model, metrics in results.items():
        print(f"\n{model}:")
        for k, v in metrics.items():
            print(f"  {k}: {v:.4f}")

    classifier.save_best_model()
    return results


if __name__ == "__main__":
    run_growth_classification()