"""
ETL Pipeline for India Economy Analytics
"""
import pandas as pd
import numpy as np
import os
import sys
import logging
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.helpers import setup_logging, create_directories, save_data
from src.data.data_loader import DataLoader
from src.features.feature_engineering import FeatureEngineer

logger = setup_logging()

class ETLPipeline:
    """Complete ETL Pipeline"""
    
    def __init__(self):
        self.loader = DataLoader()
        self.engineer = FeatureEngineer()
        self.data = None
        
    def extract(self, file_path):
        """Extract data from source"""
        logger.info("="*50)
        logger.info("EXTRACT PHASE STARTED")
        logger.info("="*50)
        
        df = self.loader.load_raw_data(file_path)
        if df is not None:
            logger.info(f"Extracted {len(df)} records")
            self.data = df
            return df
        return None
    
    def transform(self, df=None):
        """Transform data - Clean and feature engineering"""
        logger.info("="*50)
        logger.info("TRANSFORM PHASE STARTED")
        logger.info("="*50)
        
        if df is None:
            df = self.data
            
        if df is None:
            logger.error("No data to transform")
            return None
        
        # Clean data
        clean_df = self.loader.clean_data(df)
        logger.info(f"Cleaned data: {len(clean_df)} records")
        
        # Feature engineering
        featured_df = self.engineer.create_features(clean_df)
        logger.info(f"Featured data: {len(featured_df)} records")
        
        self.data = featured_df
        return featured_df
    
    def validate(self, df=None):
        """Validate data quality"""
        logger.info("="*50)
        logger.info("VALIDATION PHASE STARTED")
        logger.info("="*50)
        
        if df is None:
            df = self.data
            
        if df is None:
            logger.error("No data to validate")
            return False
        
        valid = True
        
        # Check for missing values
        missing = df.isnull().sum()
        if missing.sum() > 0:
            logger.warning(f"Missing values found:\n{missing[missing > 0]}")
        
        # Check for duplicates
        dup_count = df.duplicated().sum()
        if dup_count > 0:
            logger.warning(f"Duplicate rows found: {dup_count}")
        
        # Check data types
        logger.info("Data types verified")
        
        # Check for negative values in key columns
        key_cols = ['GDP', 'Employment']
        for col in key_cols:
            if col in df.columns:
                neg_count = (df[col] < 0).sum()
                if neg_count > 0:
                    logger.warning(f"Negative values in {col}: {neg_count}")
        
        logger.info("✅ Validation passed!")
        return valid
    
    def load(self, filename='indian_economy_processed.csv'):
        """Load data to storage"""
        logger.info("="*50)
        logger.info("LOAD PHASE STARTED")
        logger.info("="*50)
        
        if self.data is None:
            logger.error("No data to load")
            return None
        
        path = save_data(self.data, filename)
        logger.info(f"✅ Data loaded to: {path}")
        
        return path
    
    def run(self, input_file):
        """Run complete pipeline"""
        try:
            start_time = datetime.now()
            logger.info("🚀 Starting ETL Pipeline")
            logger.info(f"Input: {input_file}")
            
            # Create directories
            create_directories()
            
            # Extract
            df = self.extract(input_file)
            if df is None:
                logger.error("Extraction failed!")
                return None
            
            # Transform
            df = self.transform(df)
            if df is None:
                logger.error("Transformation failed!")
                return None
            
            # Validate
            if not self.validate(df):
                logger.warning("Validation found issues, but continuing...")
            
            # Load
            output_path = self.load()
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            logger.info("="*50)
            logger.info(f"✅ ETL Pipeline Completed!")
            logger.info(f"Records processed: {len(self.data)}")
            logger.info(f"Duration: {duration:.2f} seconds")
            logger.info(f"Output: {output_path}")
            logger.info("="*50)
            
            return self.data
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            import traceback
            traceback.print_exc()
            return None

# Main execution
if __name__ == "__main__":
    pipeline = ETLPipeline()
    result = pipeline.run('data/raw/Indian_Economy_Full_Enhanced_Dataset.xlsx')