"""
Data Loader Module
"""
import pandas as pd
import numpy as np
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import setup_logging, get_data_path, save_data

logger = setup_logging()

class DataLoader:
    """Handles data loading and initial cleaning"""
    
    def __init__(self):
        self.raw_data = None
        self.cleaned_data = None
        
    def load_raw_data(self, file_path):
        """Load raw Excel data"""
        try:
            logger.info(f"Loading data from: {file_path}")
            self.raw_data = pd.read_excel(file_path, sheet_name='Economic_Data')
            logger.info(f"Loaded {len(self.raw_data)} records")
            return self.raw_data
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return None
    
    def clean_data(self, df):
        """Clean the dataset"""
        logger.info("Starting data cleaning...")
        
        # Create copy
        df_clean = df.copy()
        
        # Standardize column names
        df_clean.columns = df_clean.columns.str.strip()
        
        # Remove duplicates
        df_clean = df_clean.drop_duplicates()
        logger.info(f"After removing duplicates: {len(df_clean)} records")
        
        # Handle missing values
        numeric_cols = df_clean.select_dtypes(include=['float64', 'int64']).columns
        for col in numeric_cols:
            df_clean[col] = df_clean[col].fillna(df_clean[col].median())
        
        categorical_cols = df_clean.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])
        
        logger.info("Missing values handled")
        
        # Remove rows with invalid GDP
        df_clean = df_clean[df_clean['GDP_Lakh_Crore'] > 0]
        
        logger.info(f"Final cleaned data: {len(df_clean)} records")
        self.cleaned_data = df_clean
        return df_clean
    
    def save_cleaned_data(self, filename='indian_economy_cleaned.csv'):
        """Save cleaned data"""
        if self.cleaned_data is not None:
            path = save_data(self.cleaned_data, filename)
            logger.info(f"Saved cleaned data to: {path}")
            return path
        return None