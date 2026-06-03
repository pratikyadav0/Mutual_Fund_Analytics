-- Query 1: Top 5 Funds ranked by total AUM scale
SELECT fund_house, MAX(aum_crores) as peak_aum_cr
FROM fact_aum
GROUP BY fund_house
ORDER BY peak_aum_cr DESC
LIMIT 5;

-- Query 2: Systemic overview of average monthly NAV values per fund code
SELECT scheme_code, STRFTIME('%Y-%m', nav_date) as nav_month, ROUND(AVG(nav_value), 2) as avg_nav
FROM fact_nav
GROUP BY scheme_code, nav_month
ORDER BY nav_month DESC, avg_nav DESC
LIMIT 10;

-- Query 3: Timeline trend analysis of overall Indian industry SIP account growth
SELECT month_year, sip_inflow_cr, active_accounts
FROM fact_sip
ORDER BY active_accounts DESC;

-- Query 4: Total transactional volume distribution grouped by Indian state borders
SELECT state, COUNT(txn_id) as total_transactions, ROUND(SUM(amount_inr), 2) as gross_capital_inr
FROM fact_transactions
GROUP BY state
ORDER BY gross_capital_inr DESC;

-- Query 5: Identifying aggressive equity profiles with expense ratio constraints below 1%
SELECT scheme_code, sharpe_ratio, sortino_ratio, alpha
FROM fact_performance
WHERE scheme_code IN (SELECT scheme_code FROM dim_fund WHERE expense_ratio < 0.01)
ORDER BY alpha DESC;

-- Query 6: Allocation mix comparison between SIP and Lumpsum funding frequencies
SELECT transaction_type, COUNT(txn_id) as transaction_count, ROUND(SUM(amount_inr), 2) as aggregate_capital
FROM fact_transactions
GROUP BY transaction_type;

-- Query 7: Demographic distribution mapping investor transaction sizes across geographic city tiers
SELECT city_tier, COUNT(txn_id) as txn_count, ROUND(AVG(amount_inr), 2) as avg_investment_size
FROM fact_transactions
GROUP BY city_tier;

-- Query 8: Top performing alpha-generating funds cross-referenced with fund manager assignments
SELECT f.scheme_name, f.fund_manager, p.alpha, p.beta
FROM dim_fund f
JOIN fact_performance p ON f.scheme_code = p.scheme_code
ORDER BY p.alpha DESC
LIMIT 5;

-- Query 9: Longitudinal correlation mapping investor age cohorts to selected fund risk tolerances
SELECT t.age_group, f.risk_category, COUNT(t.txn_id) as asset_purchase_frequency
FROM fact_transactions t
JOIN dim_fund f ON t.amfi_code = f.scheme_code
GROUP BY t.age_group, f.risk_category
ORDER BY asset_purchase_frequency DESC;

-- Query 10: Quantitative analysis of high net worth individuals mapped against payment modes
SELECT annual_income_lakh, payment_mode, COUNT(txn_id) as volume
FROM fact_transactions
WHERE annual_income_lakh > 15
GROUP BY annual_income_lakh, payment_mode
ORDER BY volume DESC
LIMIT 10;