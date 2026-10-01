"""
EcoPulse India Economic Intelligence
ETL Pipeline
"""

import pandas as pd
import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from helpers import setup_logging, create_directories, save_data
from data_loader import DataLoader
from feature_engineering import FeatureEngineer

logger = setup_logging()


class ETLPipeline:
    """Orchestrates extract, transform, validate and load stages."""

    def __init__(self):
        self.loader = DataLoader()
        self.engineer = FeatureEngineer()
        self.data = None

    def extract(self, file_path):
        """Extract data from source file."""
        logger.info("=" * 50)
        logger.info("EXTRACT PHASE")
        logger.info("=" * 50)

        df = self.loader.load_raw_data(file_path)
        if df is not None:
            logger.info(f"Extracted {len(df)} records")
            self.data = df
        return df

    def transform(self, df=None):
        """Apply cleaning and feature engineering."""
        logger.info("=" * 50)
        logger.info("TRANSFORM PHASE")
        logger.info("=" * 50)

        if df is None:
            df = self.data

        if df is None:
            logger.error("No data available for transformation")
            return None

        clean_df = self.loader.clean_data(df)
        featured_df = self.engineer.create_features(clean_df)

        self.data = featured_df
        return featured_df

    def validate(self, df=None):
        """Run data quality checks."""
        logger.info("=" * 50)
        logger.info("VALIDATION PHASE")
        logger.info("=" * 50)

        if df is None:
            df = self.data

        if df is None:
            logger.error("No data available for validation")
            return False

        missing = df.isnull().sum()
        if missing.sum() > 0:
            logger.warning(f"Missing values detected: {missing[missing > 0].to_dict()}")

        duplicates = df.duplicated().sum()
        if duplicates > 0:
            logger.warning(f"Duplicate rows detected: {duplicates}")

        logger.info("Validation completed successfully")
        return True

    def load(self, filename='ecopulse_processed.csv'):
        """Persist processed dataset."""
        logger.info("=" * 50)
        logger.info("LOAD PHASE")
        logger.info("=" * 50)

        if self.data is None:
            logger.error("No data available to load")
            return None

        path = save_data(self.data, filename)
        logger.info(f"Data saved: {path}")
        return path

    def run(self, input_file):
        """Execute the full ETL pipeline."""
        try:
            start_time = datetime.now()
            logger.info(f"Pipeline started: {input_file}")

            create_directories()

            df = self.extract(input_file)
            if df is None:
                return None

            df = self.transform(df)
            if df is None:
                return None

            self.validate(df)
            output_path = self.load()

            duration = (datetime.now() - start_time).total_seconds()

            logger.info("=" * 50)
            logger.info("PIPELINE COMPLETED")
            logger.info(f"Records processed: {len(self.data)}")
            logger.info(f"Duration: {duration:.2f}s")
            logger.info(f"Output: {output_path}")
            logger.info("=" * 50)

            return self.data

        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            import traceback
            traceback.print_exc()
            return None


if __name__ == "__main__":
    pipeline = ETLPipeline()
    pipeline.run('data/raw/Ecopulse Economy Dataset.csv')