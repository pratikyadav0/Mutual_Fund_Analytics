import pandas as pd
import sqlite3
import os

# setting up folder paths
raw_dir = "data/raw"
processed_dir = "data/processed"
db_path = "data/db/bluestock_mf.db"

# creating the processed folder if it's missing
if not os.path.exists(processed_dir):
    os.makedirs(processed_dir)

# connecting to sqlite database
db_conn = sqlite3.connect(db_path)

print("Starting to clean files...")

# ==========================================
# CLEANING THE NAV HISTORY FILE
# ==========================================
print("Working on NAV History file...")

# load the raw csv file
nav_df = pd.read_csv(os.path.join(raw_dir, "02_nav_history.csv"))

# renaming columns so they match our table headers perfectly
nav_df.columns = ['scheme_code', 'nav_date', 'nav_value']

# fix the date column format
nav_df['nav_date'] = pd.to_datetime(nav_df['nav_date'])

# remove rows where nav value is 0 or negative
nav_df = nav_df[nav_df['nav_value'] > 0]

# drop duplicate entries if there are any
nav_df = nav_df.drop_duplicates(subset=['scheme_code', 'nav_date'])

# sort by code and date to put them in proper order
nav_df = nav_df.sort_values(by=['scheme_code', 'nav_date'])

# filling missing values for weekends and holidays using ffill and bfill
nav_df = nav_df.groupby('scheme_code').ffill().bfill()

# reset the index to keep scheme_code as a normal column
if 'scheme_code' not in nav_df.columns:
    nav_df = nav_df.reset_index()

# change date format back to string text for sql saving
nav_df['nav_date'] = pd.to_datetime(nav_df['nav_date']).dt.strftime('%Y-%m-%d')

# save to processed folder and load into database table
nav_df.to_csv(os.path.join(processed_dir, "cleaned_nav_history.csv"), index=False)
nav_df.to_sql("fact_nav", db_conn, if_exists="replace", index=False)
print("NAV History file done!")


# ==========================================
# CLEANING INVESTOR TRANSACTIONS FILE
# ==========================================
print("Working on Investor Transactions file...")

# read the raw transaction csv
txn_df = pd.read_csv(os.path.join(raw_dir, "08_investor_transactions.csv"))

# fix transaction date column format
txn_df['transaction_date'] = pd.to_datetime(txn_df['transaction_date']).dt.strftime('%Y-%m-%d')

# ensure amount is numeric and more than 0
txn_df['amount_inr'] = pd.to_numeric(txn_df['amount_inr'])
txn_df = txn_df[txn_df['amount_inr'] > 0]

# clean transaction type text - remove extra spaces and capitalize first letter
txn_df['transaction_type'] = txn_df['transaction_type'].str.strip().str.capitalize()

# save csv and load into database table
txn_df.to_csv(os.path.join(processed_dir, "cleaned_investor_transactions.csv"), index=False)
txn_df.to_sql("fact_transactions", db_conn, if_exists="replace", index=False)
print("Investor Transactions file done!")


# ==========================================
# LOADING THE REST OF THE CSV FILES
# ==========================================
print("Loading master files into database...")

# loading fund master csv
m_df = pd.read_csv(os.path.join(raw_dir, "01_fund_master.csv"))
m_df.to_csv(os.path.join(processed_dir, "cleaned_fund_master.csv"), index=False)
m_df.to_sql("dim_fund", db_conn, if_exists="replace", index=False)

# loading aum csv
aum_df = pd.read_csv(os.path.join(raw_dir, "03_aum_by_fund_house.csv"))
aum_df.to_sql("fact_aum", db_conn, if_exists="replace", index=False)

# loading sip inflows csv
sip_df = pd.read_csv(os.path.join(raw_dir, "04_monthly_sip_inflows.csv"))
sip_df.to_sql("fact_sip", db_conn, if_exists="replace", index=False)

# loading performance metrics csv
perf_df = pd.read_csv(os.path.join(raw_dir, "07_scheme_performance.csv"))
# rename columns to match our sql schema fields
perf_df = perf_df.rename(columns={
    '1yr_cagr': 'cagr_1yr',
    '3yr_cagr': 'cagr_3yr',
    '5yr_cagr': 'cagr_5yr'
})
perf_df.to_sql("fact_performance", db_conn, if_exists="replace", index=False)

# close the connection
db_conn.close()

print("All tasks finished successfully!")