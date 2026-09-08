"""
Feature Engineering Module
"""
import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import setup_logging, save_data

logger = setup_logging()

class FeatureEngineer:
    """Handles feature engineering"""
    
    def __init__(self):
        self.featured_data = None
    
    def create_features(self, df):
        """Create new features from existing data"""
        logger.info("Creating new features...")
        
        df_fe = df.copy()
        
        # Rename columns to simpler names
        rename_cols = {
            'GDP_Lakh_Crore': 'GDP',
            'Growth_%': 'Growth_Rate',
            'Employment_Million': 'Employment',
            'Exports_Crore': 'Exports',
            'Imports_Crore': 'Imports',
            'FDI_Crore': 'FDI',
            'Inflation_%': 'Inflation',
            'Tax_Revenue_Crore': 'Tax_Revenue'
        }
        df_fe = df_fe.rename(columns=rename_cols)
        
        # 1. Trade Balance
        df_fe['Trade_Balance'] = df_fe['Exports'] - df_fe['Imports']
        
        # 2. GDP per Employment
        df_fe['GDP_per_Employment'] = df_fe['GDP'] / df_fe['Employment']
        
        # 3. Trade Openness
        df_fe['Trade_Openness'] = (df_fe['Exports'] + df_fe['Imports']) / df_fe['GDP']
        
        # 4. FDI to GDP Ratio
        df_fe['FDI_to_GDP'] = df_fe['FDI'] / df_fe['GDP']
        
        # 5. Tax Efficiency
        df_fe['Tax_Efficiency'] = df_fe['Tax_Revenue'] / df_fe['GDP']
        
        # 6. Growth Momentum (lagged)
        df_fe['Growth_Momentum'] = df_fe.groupby('Sector')['Growth_Rate'].shift(1)
        
        # 7. Economic Cycle
        avg_growth = df_fe['Growth_Rate'].mean()
        df_fe['Economic_Cycle'] = np.where(df_fe['Growth_Rate'] > avg_growth, 'Expansion', 'Contraction')
        
        # 8. Performance Score
        df_fe['Performance_Score'] = (
            (df_fe['Growth_Rate'] / df_fe['Growth_Rate'].max()) +
            (df_fe['GDP'] / df_fe['GDP'].max()) +
            (df_fe['Employment'] / df_fe['Employment'].max())
        ) / 3
        
        # 9. GDP Category
        df_fe['GDP_Category'] = pd.qcut(df_fe['GDP'], 
                                        q=3, 
                                        labels=['Low', 'Medium', 'High'])
        
        # 10. Growth Category
        df_fe['Growth_Category'] = pd.cut(df_fe['Growth_Rate'],
                                         bins=[-float('inf'), 0, 3, 6, float('inf')],
                                         labels=['Negative', 'Low', 'Moderate', 'High'])
        
        # 11. Inflation Category
        df_fe['Inflation_Category'] = pd.cut(df_fe['Inflation'],
                                            bins=[-float('inf'), 3, 5, 7, float('inf')],
                                            labels=['Low', 'Moderate', 'High', 'Very High'])
        
        # 12. Quarter Number
        if 'Quarter' in df_fe.columns:
            df_fe['Quarter_Number'] = df_fe['Quarter'].str.extract('(\d+)').astype(float)
        
        # 13. Period Label
        df_fe['Period'] = df_fe['Year'].astype(str) + ' ' + df_fe['Quarter'].astype(str)
        
        logger.info(f"Added new features")
        logger.info(f"Total columns: {len(df_fe.columns)}")
        
        self.featured_data = df_fe
        return df_fe
    
    def save_featured_data(self, filename='indian_economy_featured.csv'):
        """Save featured data"""
        if self.featured_data is not None:
            path = save_data(self.featured_data, filename)
            logger.info(f"Saved featured data to: {path}")
            return path
        return None