
SELECT transaction_date
FROM fact_transactions
LIMIT 5;
SELECT
    EXTRACT(YEAR FROM CAST(transaction_date AS DATE)) AS year,
    SUM(amount_inr) AS total_sip
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY 1
ORDER BY 1;
-- =====================================================
-- 1. Top 5 Funds by AUM
-- =====================================================
SELECT
    scheme_name,
    aum_crore
FROM fact_performance
ORDER BY aum_crore DESC
LIMIT 5;
-- =====================================================
-- 2. Average NAV Per Month
-- =====================================================
SELECT
    DATE_TRUNC('month', CAST(date AS DATE)) AS month,
    AVG(nav) AS avg_nav
FROM fact_nav
GROUP BY 1
ORDER BY 1;
-- =====================================================
-- 3. SIP Transactions by Year
-- =====================================================
SELECT
    EXTRACT(YEAR FROM CAST(transaction_date AS DATE)) AS year,
    SUM(amount_inr) AS total_sip
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY 1
ORDER BY 1;
-- =====================================================
-- 4. Transactions by State
-- =====================================================
SELECT
    state,
    SUM(amount_inr) AS total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_amount DESC;
-- =====================================================
-- 5. Funds with Expense Ratio < 1%
-- =====================================================
SELECT
    scheme_name,
    expense_ratio_pct
FROM fact_performance
WHERE expense_ratio_pct < 1
ORDER BY expense_ratio_pct;
-- =====================================================
-- 6. Top 5 Funds by 5-Year Return
-- =====================================================
SELECT
    scheme_name,
    return_5yr_pct
FROM fact_performance
ORDER BY return_5yr_pct DESC
LIMIT 5;
-- =====================================================
-- 7. Category-wise Total AUM
-- =====================================================
SELECT
    category,
    SUM(aum_crore) AS total_aum
FROM fact_performance
GROUP BY category
ORDER BY total_aum DESC;
-- =====================================================
-- 8. Average NAV by Fund
-- =====================================================
SELECT
    amfi_code,
    AVG(nav) AS avg_nav
FROM fact_nav
GROUP BY amfi_code
ORDER BY avg_nav DESC;
-- =====================================================
-- 9. Top 10 Funds by Sharpe Ratio
-- =====================================================
SELECT
    scheme_name,
    sharpe_ratio
FROM fact_performance
ORDER BY sharpe_ratio DESC
LIMIT 10;
-- =====================================================
-- 10. Investor Count by State
-- =====================================================
SELECT
    state,
    COUNT(DISTINCT investor_id) AS investor_count
FROM fact_transactions
GROUP BY state
ORDER BY investor_count DESC;
-- Fund Managers Handling Most Funds

SELECT
    fund_manager,
    COUNT(*) AS number_of_funds
FROM dim_fund
GROUP BY fund_manager
ORDER BY number_of_funds DESC;