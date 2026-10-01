"""
EcoPulse India Economic Intelligence
Main Runner
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from helpers import setup_logging, create_directories
from etl_pipeline import ETLPipeline

logger = setup_logging()


def main():
    """Execute the EcoPulse pipeline."""
    print("=" * 60)
    print("ECOPULSE INDIA ECONOMIC INTELLIGENCE")
    print("=" * 60)

    create_directories()

    # ✅ CHANGED FILE NAME HERE
    input_file = 'data/raw/Ecopulse Economy Dataset.csv'

    if not os.path.exists(input_file):
        logger.error(f"Input file not found: {input_file}")
        print(f"\nError: Please place the dataset at: {input_file}")
        return

    pipeline = ETLPipeline()
    data = pipeline.run(input_file)

    if data is not None:
        print("\n" + "=" * 60)
        print("PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print(f"\nData shape: {data.shape}")
        print(f"Columns: {len(data.columns)}")
        print(f"Years: {data['Year'].min()} - {data['Year'].max()}")
        print(f"Sectors: {data['Sector'].nunique()}")
        print(f"\nOutput: data/processed/ecopulse_processed.csv")
        print("\nSample Data:")
        print(data[['Year', 'Sector', 'GDP', 'Growth_Rate']].head(5))
        print("\n" + "=" * 60)
        print("Next Step: streamlit run app/streamlit_app.py")
        print("=" * 60)
    else:
        print("\nPipeline failed. Check logs for details.")


if __name__ == "__main__":
    main()