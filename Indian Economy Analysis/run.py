"""
Main Runner for India Economy Analytics
"""
import os
import sys
import pandas as pd

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.utils.helpers import setup_logging, create_directories
from pipeline.etl_pipeline import ETLPipeline

logger = setup_logging()

def main():
    """Main execution function"""
    print("="*60)
    print("🇮🇳 INDIA ECONOMY ANALYTICS - PROJECT RUNNER")
    print("="*60)
    
    # Create directories
    create_directories()
    
    # File path
    input_file = 'data/raw/Indian_Economy_Full_Enhanced_Dataset.xlsx'
    
    # Check if file exists
    if not os.path.exists(input_file):
        logger.error(f"Input file not found: {input_file}")
        print(f"\n❌ Error: Please place your Excel file at: {input_file}")
        print("\n📁 Folder structure should be:")
        print("   India-Economy-Analytics/")
        print("   └── data/")
        print("       └── raw/")
        print("           └── Indian_Economy_Full_Enhanced_Dataset.xlsx")
        return
    
    # Run ETL Pipeline
    pipeline = ETLPipeline()
    data = pipeline.run(input_file)
    
    if data is not None:
        print("\n" + "="*60)
        print("✅ PIPELINE COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"\n📊 Data shape: {data.shape}")
        print(f"📋 Columns: {len(data.columns)}")
        print(f"📅 Years: {data['Year'].min()} - {data['Year'].max()}")
        print(f"🏭 Sectors: {data['Sector'].nunique()}")
        print(f"\n📁 Output: data/processed/indian_economy_processed.csv")
        print("\n🔍 Sample Data:")
        print(data[['Year', 'Sector', 'GDP', 'Growth_Rate']].head(10))
        print("\n" + "="*60)
        print("🚀 Next Step: Run Streamlit App")
        print("   streamlit run app/streamlit_app.py")
        print("="*60)
    else:
        print("\n❌ Pipeline failed! Check logs for details.")

if __name__ == "__main__":
    main()