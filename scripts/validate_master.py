import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

def analyze_and_validate():
    print("=" * 60)
    print("RUNNING TASK 6 & 7: MASTER VALIDATION WORKFLOW")
    print("=" * 60)
    
    # Load required datasets
    master_path = RAW_DATA_DIR / "01_fund_master.csv"
    nav_path = RAW_DATA_DIR / "02_nav_history.csv"
    
    if not master_path.exists() or not nav_path.exists():
        print("❌ Error: Missing fundamental datasets for profiling.")
        return
        
    df_master = pd.read_csv(master_path)
    df_nav = pd.read_csv(nav_path)
    
    # Task 6: Explore metrics inside Fund Master
    print("\n🏢 [TASK 6] FUND MASTER PROFILE:")
    print(f"• Unique Fund Houses: {df_master['fund_house'].nunique()}")
    print(f"• Unique Categories: {df_master['category'].nunique()}")
    print(f"• Unique Sub-Categories: {df_master['sub_category'].nunique()}")
    print(f"• Registered Risk Grades: {df_master['risk_category'].dropna().unique().tolist()}")
    
    # Task 7: Cross-Validate AMFI Reference Codes
    print("\n🔍 [TASK 7] AMFI CODE DATA QUALITY CHECKS:")
    master_codes = set(df_master['amfi_code'].unique())
    nav_codes = set(df_nav['amfi_code'].unique())
    
    missing_in_nav = master_codes - nav_codes
    
    print(f"• Total codes in Fund Master: {len(master_codes)}")
    print(f"• Total codes found in NAV History: {len(nav_codes)}")
    
    if len(missing_in_nav) == 0:
        print("✅ SUCCESS SUMMARY: Every AMFI code in fund_master maps completely to nav_history!")
    else:
        print(f"⚠️ ANOMALY ALERT: {len(missing_in_nav)} master codes are missing from history sheets: {missing_in_nav}")
    print("=" * 60)

if __name__ == "__main__":
    analyze_and_validate()