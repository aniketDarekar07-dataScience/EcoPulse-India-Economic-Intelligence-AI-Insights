"""
Helper functions for India Economy Analytics
"""
import pandas as pd
import numpy as np
import logging
import os
from datetime import datetime

def setup_logging(log_file='logs/economy.log'):
    """Setup logging configuration"""
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
    """Create necessary directories"""
    dirs = ['data/raw', 'data/processed', 'logs', 'models', 'reports']
    for d in dirs:
        os.makedirs(d, exist_ok=True)

def get_data_path(filename):
    """Get absolute path for data files"""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base_dir, 'data', 'processed', filename)

def save_data(df, filename, format='csv'):
    """Save dataframe to file"""
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
    """Load data from file"""
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
    """Calculate growth rate"""
    if previous == 0:
        return 0
    return ((current - previous) / previous) * 100

def get_quarter(month):
    """Get quarter from month"""
    if month in [1,2,3]: return 1
    elif month in [4,5,6]: return 2
    elif month in [7,8,9]: return 3
    else: return 4

def get_financial_year(year, month):
    """Get financial year"""
    if month >= 4:
        return f"{year}-{str(year+1)[-2:]}"
    else:
        return f"{year-1}-{str(year)[-2:]}"