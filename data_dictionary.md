# 📊 Mutual Fund Analytics — Data Dictionary

This document details the production relational tables deployed in `bluestock_mf.db` to drive backend analytics and upcoming dashboard metrics.

---

## 🏛️ Dimension Tables

### 1. `dim_fund`
Stores descriptive information and properties for all active AMFI Mutual Fund schemes.
* `scheme_code` (INTEGER, Primary Key): Unique AMFI code identifying the fund.
* `scheme_name` (TEXT): Official title name of the fund setup.
* `fund_house` (TEXT): Parent asset management company (AMC) group.
* `category` (TEXT): Broad grouping class (e.g., Equity, Debt).
* `sub_category` (TEXT): Granular market focus (e.g., Large Cap, Mid Cap).
* `risk_category` (TEXT): Risk assessment score tier assigned to the profile.
* `expense_ratio` (REAL): Annualized operational management fee percentage.
* `fund_manager` (TEXT): Primary analyst executing transactions for the pool.

### 2. `dim_date`
Provides robust date attributes to perform time-series analytics.
* `date_string` (TEXT, Primary Key): Date index matching `YYYY-MM-DD`.
* `calendar_year` (INTEGER): Numeric year signature (e.g., 2025).
* `calendar_month` (INTEGER): Sequential numeric index of month (1–12).
* `month_name` (TEXT): Literal string translation (e.g., "December").
* `day_of_week` (TEXT): Specific daily designation (e.g., "Sunday").

---

## 📈 Fact Tables

### 3. `fact_nav`
Stores a long-form timeline profile of clean, day-to-day asset valuation indices.
* `nav_id` (INTEGER, Primary Key Auto-Increment): Sequence row index tracking ID.
* `scheme_code` (INTEGER, Foreign Key): Linked back to `dim_fund`.
* `nav_date` (TEXT, Foreign Key): Linked back to calendar dimensions via `dim_date`.
* `nav_value` (REAL): Net Asset Value price calculated at market close.

### 4. `fact_transactions`
Captures investor interaction trends across all 12 tracked Indian states.
* `txn_id` (INTEGER, Primary Key Auto-Increment): Unique signature code tracking transaction occurrences.
* `investor_id` (TEXT): Masked unique client identifier tracking repeat business.
* `transaction_date` (TEXT, Foreign Key): System tracking index string.
* `amfi_code` (INTEGER, Foreign Key): Key linking details to scheme properties.
* `transaction_type` (TEXT): Standardized categorization tracking (SIP, Lumpsum, Redemption).
* `amount_inr` (REAL): Total raw cash value transacted.
* `state` / `city` / `city_tier` (TEXT): Demographic geographic location anchors.
* `age_group` / `gender` / `annual_income_lakh` (TEXT/REAL): Investor biometric traits.

### 5. `fact_performance`
Locks down relative statistical scoring parameters computed for the fund options.
* `scheme_code` (INTEGER, Primary Key): Core identifier link.
* `cagr_1yr` / `cagr_3yr` / `cagr_5yr` (REAL): Compound Annual Growth Rates.
* `sharpe_ratio` / `sortino_ratio` (REAL): Risk-adjusted performance return multipliers.
* `alpha` / `beta` (REAL): Operational risk adjustments compared against Nifty benchmarks.
* `max_drawdown` / `std_dev` (REAL): Core downside protective metrics.