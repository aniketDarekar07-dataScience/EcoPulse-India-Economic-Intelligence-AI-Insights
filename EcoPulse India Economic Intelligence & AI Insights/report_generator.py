"""
EcoPulse India Economic Intelligence
AI Report Generator
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from helpers import setup_logging, load_data

logger = setup_logging()


class EconomicReportGenerator:
    """Generates data-driven economic insights."""

    def __init__(self):
        self.insights = []

    def generate_insights(self, df):
        """Produce structured economic insights."""
        top_gdp = df.groupby('Sector')['GDP'].sum()
        top_gdp_sector = top_gdp.idxmax()

        top_growth = df.groupby('Sector')['Growth_Rate'].mean()
        top_growth_sector = top_growth.idxmax()

        top_fdi = df.groupby('Sector')['FDI'].sum()
        top_fdi_sector = top_fdi.idxmax()

        top_emp = df.groupby('Sector')['Employment'].sum()
        top_emp_sector = top_emp.idxmax()

        avg_inflation = df['Inflation'].mean()
        avg_growth = df['Growth_Rate'].mean()

        self.insights = [
            f"Top GDP contributor: {top_gdp_sector} (Rs {top_gdp.max():.2f} Lakh Cr)",
            f"Highest growth sector: {top_growth_sector} ({top_growth.max():.2f}%)",
            f"Leading FDI destination: {top_fdi_sector} (Rs {top_fdi.max():.2f} Cr)",
            f"Largest employer: {top_emp_sector} ({top_emp.max():.2f} Million)",
            f"Average inflation across period: {avg_inflation:.2f}%",
            f"Average growth rate: {avg_growth:.2f}%"
        ]

        return self.insights

    def save_report(self, path='reports/economic_insights.txt'):
        """Persist insights to file."""
        os.makedirs('reports', exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write("ECOPULSE ECONOMIC INSIGHTS\n")
            f.write("=" * 50 + "\n\n")
            for i, insight in enumerate(self.insights, 1):
                f.write(f"{i}. {insight}\n")
        logger.info(f"Report saved: {path}")
        return path


def run_report_generation():
    """Execute insight generation."""
    df = load_data('ecopulse_processed.csv')
    if df is None:
        logger.error("Processed data not found")
        return

    generator = EconomicReportGenerator()
    insights = generator.generate_insights(df)

    print("\n" + "=" * 60)
    print("AI-GENERATED ECONOMIC INSIGHTS")
    print("=" * 60)
    for i, insight in enumerate(insights, 1):
        print(f"  {i}. {insight}")

    generator.save_report()
    return insights


if __name__ == "__main__":
    run_report_generation()