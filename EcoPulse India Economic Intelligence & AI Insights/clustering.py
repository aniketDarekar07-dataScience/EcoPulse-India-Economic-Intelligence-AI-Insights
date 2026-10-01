"""
EcoPulse India Economic Intelligence
K-Means Clustering
"""

import pandas as pd
import numpy as np
import os
import sys
import joblib
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from helpers import setup_logging, load_data

logger = setup_logging()


class EconomicClusterer:
    """Groups economic records using K-Means."""

    def __init__(self):
        self.scaler = StandardScaler()
        self.model = None
        self.optimal_k = None

    def find_optimal_clusters(self, X, max_k=8):
        """Determine optimal cluster count using silhouette score."""
        scores = {}
        for k in range(2, max_k + 1):
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = kmeans.fit_predict(X)
            scores[k] = silhouette_score(X, labels)

        self.optimal_k = max(scores, key=scores.get)
        logger.info(f"Optimal clusters: {self.optimal_k}")
        return scores

    def fit(self, df):
        """Fit clustering model on economic features."""
        feature_cols = ['GDP', 'Growth_Rate', 'Employment', 'FDI', 'Inflation']
        X = df[feature_cols].fillna(0)

        X_scaled = self.scaler.fit_transform(X)
        self.find_optimal_clusters(X_scaled)

        self.model = KMeans(n_clusters=self.optimal_k, random_state=42, n_init=10)
        df = df.copy()
        df['Cluster'] = self.model.fit_predict(X_scaled)

        return df

    def analyze_clusters(self, df):
        """Profile each cluster."""
        profile = df.groupby('Cluster').agg({
            'GDP': 'mean',
            'Growth_Rate': 'mean',
            'Employment': 'mean',
            'FDI': 'mean',
            'Inflation': 'mean'
        }).round(2)

        profile['Count'] = df.groupby('Cluster').size()
        return profile

    def save_model(self):
        """Persist clustering model."""
        os.makedirs('models', exist_ok=True)
        joblib.dump(self.model, 'models/clustering_model.pkl')
        joblib.dump(self.scaler, 'models/clustering_scaler.pkl')
        logger.info("Clustering model saved")


def run_clustering():
    """Execute clustering pipeline."""
    df = load_data('ecopulse_processed.csv')
    if df is None:
        logger.error("Processed data not found")
        return

    clusterer = EconomicClusterer()
    clustered_df = clusterer.fit(df)
    profile = clusterer.analyze_clusters(clustered_df)

    print("\n" + "=" * 60)
    print("CLUSTER PROFILES")
    print("=" * 60)
    print(profile)

    clusterer.save_model()
    return clustered_df, profile


if __name__ == "__main__":
    run_clustering()