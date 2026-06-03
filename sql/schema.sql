-- 1. Dimension Fund Table
CREATE TABLE IF NOT EXISTS dim_fund (
    scheme_code INTEGER PRIMARY KEY,
    scheme_name TEXT NOT NULL,
    fund_house TEXT,
    category TEXT,
    sub_category TEXT,
    risk_category TEXT,
    expense_ratio REAL,
    fund_manager TEXT
);

-- 2. Dimension Date Table 
CREATE TABLE IF NOT EXISTS dim_date (
    date_string TEXT PRIMARY KEY,
    calendar_year INTEGER,
    calendar_month INTEGER,
    month_name TEXT,
    day_of_week TEXT
);

-- 3. Fact NAV Table
CREATE TABLE IF NOT EXISTS fact_nav (
    nav_id INTEGER PRIMARY KEY AUTOINCREMENT,
    scheme_code INTEGER,
    nav_date TEXT,
    nav_value REAL,
    FOREIGN KEY (scheme_code) REFERENCES dim_fund(scheme_code),
    FOREIGN KEY (nav_date) REFERENCES dim_date(date_string)
);

-- 4. Fact AUM Table
CREATE TABLE IF NOT EXISTS fact_aum (
    aum_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_house TEXT,
    quarter_date TEXT,
    aum_crores REAL
);

-- 5. Fact SIP Table
CREATE TABLE IF NOT EXISTS fact_sip (
    sip_id INTEGER PRIMARY KEY AUTOINCREMENT,
    month_year TEXT,
    sip_inflow_cr REAL,
    active_accounts REAL
);

-- 6. Fact Performance Table 
CREATE TABLE IF NOT EXISTS fact_performance (
    scheme_code INTEGER PRIMARY KEY,
    cagr_1yr REAL,
    cagr_3yr REAL,
    cagr_5yr REAL,
    sharpe_ratio REAL,
    sortino_ratio REAL,
    alpha REAL,
    beta REAL,
    max_drawdown REAL,
    std_dev REAL,
    FOREIGN KEY (scheme_code) REFERENCES dim_fund(scheme_code)
);

-- 7. Fact Transactions Table
CREATE TABLE IF NOT EXISTS fact_transactions (
    txn_id INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id TEXT,
    transaction_date TEXT,
    amfi_code INTEGER,
    transaction_type TEXT,
    amount_inr REAL,
    state TEXT,
    city TEXT,
    city_tier TEXT,
    age_group TEXT,
    gender TEXT,
    annual_income_lakh REAL,
    payment_mode TEXT,
    kyc_status TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(scheme_code),
    FOREIGN KEY (transaction_date) REFERENCES dim_date(date_string)
);