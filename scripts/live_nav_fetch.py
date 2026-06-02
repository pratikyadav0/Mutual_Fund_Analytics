import requests
import pandas as pd
from pathlib import Path

# Setup paths based on project rubrics
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

# The target scheme codes provided in your Day 1 requirements
SCHEMES = {
    "125497": "HDFC_Top_100_Direct",
    "119551": "SBI_Bluechip",
    "120503": "ICICI_Bluechip",
    "118632": "Nippon_Large_Cap",
    "119092": "Axis_Bluechip",
    "120841": "Kotak_Bluechip"
}

def fetch_live_nav():
    print("=" * 60)
    print("STARTING LIVE NAV FETCH FROM MFAPI.IN")
    print("=" * 60)
    
    for code, name in SCHEMES.items():
        url = f"https://api.mfapi.in/mf/{code}"
        print(f"\n📡 Fetching data for {name} (Code: {code})...")
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                # Extract meta and nav details from the JSON response
                meta = data.get("meta", {})
                nav_list = data.get("data", [])
                
                if not nav_list:
                    print(f"⚠️ No historical NAV data found for {name}.")
                    continue
                
                # Convert list to DataFrame
                df = pd.DataFrame(nav_list)
                
                # Add scheme identifying metadata columns
                df["scheme_code"] = code
                df["scheme_name"] = meta.get("scheme_name", name)
                
                # Save as raw CSV
                output_file = RAW_DATA_DIR / f"live_raw_{code}_{name}.csv"
                df.to_csv(output_file, index=False)
                print(f"✅ Saved {len(df)} records to: {output_file.name}")
                
            else:
                print(f"❌ Failed to fetch {name}. HTTP Status: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error encountered while connecting for {name}: {str(e)}")
            
    print("\n" + "=" * 60)
    print("LIVE NAV FETCH COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    fetch_live_nav()