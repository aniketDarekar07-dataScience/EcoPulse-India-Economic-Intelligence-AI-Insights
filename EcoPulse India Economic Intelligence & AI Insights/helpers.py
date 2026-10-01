"""
EcoPulse India Economic Intelligence
Utility Functions
"""

import os
import logging
import pandas as pd


def setup_logging(log_file='logs/ecopulse.log'):
    """Configure application logging."""
    os.makedirs('logs', exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


def create_directories():
    """Create required project directories."""
    directories = [
        'data/raw',
        'data/processed',
        'logs',
        'models',
        'reports',
        'screenshots'
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


def save_data(df, filename, format='csv'):
    """Save dataframe to processed directory."""
    os.makedirs('data/processed', exist_ok=True)
    path = os.path.join('data/processed', filename)

    if format == 'csv':
        df.to_csv(path, index=False)
    elif format == 'parquet':
        df.to_parquet(path, index=False)
    elif format == 'excel':
        df.to_excel(path, index=False)

    return path


def load_data(filename, format='csv'):
    """Load processed data."""
    path = os.path.join('data/processed', filename)
    if not os.path.exists(path):
        return None

    if format == 'csv':
        return pd.read_csv(path)
    elif format == 'parquet':
        return pd.read_parquet(path)
    elif format == 'excel':
        return pd.read_excel(path)

    return None


def calculate_growth_rate(current, previous):
    """Calculate percentage growth rate."""
    if previous == 0:
        return 0
    return ((current - previous) / previous) * 100