"""
EcoPulse India Economic Intelligence
Data Loader Module
"""

# pyright: reportMissingModuleSource=false
try:
    import pandas as pd
except ImportError as exc:
    raise ImportError(
        "pandas is required to run EcoPulse. Install it with: pip install pandas"
    ) from exc

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from helpers import setup_logging, save_data

logger = setup_logging()


class DataLoader:
    """Handles data loading and cleaning operations."""

    def __init__(self):
        self.raw_data = None
        self.cleaned_data = None

    def load_raw_data(self, file_path):
        """Load raw CSV data from source."""
        try:
            logger.info(f"Loading data from: {file_path}")
            self.raw_data = pd.read_csv(file_path)
            logger.info(f"Loaded {len(self.raw_data)} records")
            return self.raw_data
        except Exception as e:
            logger.error(f"Failed to load data: {e}")
            return None

    def clean_data(self, df):
        """Clean and validate the dataset."""
        logger.info("Starting data cleaning")

        df_clean = df.copy()
        df_clean.columns = df_clean.columns.str.strip()

        initial_count = len(df_clean)
        df_clean = df_clean.drop_duplicates()
        logger.info(f"Removed {initial_count - len(df_clean)} duplicates")

        numeric_cols = df_clean.select_dtypes(include=['float64', 'int64']).columns
        for col in numeric_cols:
            df_clean[col] = df_clean[col].fillna(df_clean[col].median())

        categorical_cols = df_clean.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])

        if 'GDP_Lakh_Crore' in df_clean.columns:
            df_clean = df_clean[df_clean['GDP_Lakh_Crore'] > 0]

        logger.info(f"Final cleaned data: {len(df_clean)} records")
        self.cleaned_data = df_clean
        return df_clean

    def save_cleaned_data(self, filename='ecopulse_cleaned.csv'):
        """Save cleaned data to processed folder."""
        if self.cleaned_data is not None:
            path = save_data(self.cleaned_data, filename)
            logger.info(f"Saved cleaned data: {path}")
            return path
        return None