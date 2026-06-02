import pandas as pd
from pathlib import Path

# Setup cross-platform path handling as required by rubric
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

# List of all 10 datasets to inspect
datasets = [
    "01_fund_master.csv",
    "02_nav_history.csv",
    "03_aum_by_fund_house.csv",
    "04_monthly_sip_inflows.csv",
    "05_category_inflows.csv",
    "06_industry_folio_count.csv",
    "07_scheme_performance.csv",
    "08_investor_transactions.csv",
    "09_portfolio_holdings.csv",
    "10_benchmark_indices.csv"
]

def ingest_and_inspect():
    print("=" * 60)
    print("STARTING DATA INGESTION & QUALITY INSPECTION")
    print("=" * 60)
    
    for filename in datasets:
        file_path = RAW_DATA_DIR / filename
        print(f"\n[🔄 LOADING] {filename}...")
        
        if not file_path.exists():
            print(f"❌ Error: File not found at {file_path}")
            continue
            
        # Load dataset
        df = pd.read_csv(file_path)
        
        # Print Shape, Data Types, and Head as required by Task 3
        print(f"📊 Shape: {df.shape[0]} rows, {df.shape[1]} columns")
        print("\n🧬 Data Types:")
        print(df.dtypes)
        print("\n🔝 First 3 Rows:")
        print(df.head(3))
        print("-" * 60)

if __name__ == "__main__":
    ingest_and_inspect()