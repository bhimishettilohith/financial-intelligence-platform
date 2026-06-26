-- ==========================================
-- Query 1: Total Companies
-- ==========================================

SELECT COUNT(*) AS total_companies
FROM companies;

-- ==========================================
-- Query 2: Profit & Loss Row Count
-- ==========================================

SELECT COUNT(*) AS total_pl_records
FROM profitandloss;

-- ==========================================
-- Query 3: Balance Sheet Row Count
-- ==========================================

SELECT COUNT(*) AS total_bs_records
FROM balancesheet;

-- ==========================================
-- Query 4: Cash Flow Row Count
-- ==========================================

SELECT COUNT(*) AS total_cf_records
FROM cashflow;

-- ==========================================
-- Query 5: Stock Price Row Count
-- ==========================================

SELECT COUNT(*) AS total_price_records
FROM stock_prices;

-- ==========================================
-- Query 6: Foreign Key Validation
-- ==========================================

PRAGMA foreign_key_check;

-- ==========================================
-- Query 7: Companies with Less Than
-- 5 Years of Financial History
-- ==========================================

SELECT
company_id,
COUNT(*) AS records
FROM profitandloss
GROUP BY company_id
HAVING COUNT(*) < 5
ORDER BY records;

-- ==========================================
-- Query 8: Year Coverage Per Company
-- ==========================================

SELECT
company_id,
MIN(year) AS first_year,
MAX(year) AS last_year,
COUNT(*) AS total_records
FROM profitandloss
GROUP BY company_id
ORDER BY total_records ASC;

-- ==========================================
-- Query 9: Top 10 Companies by
-- Average Sales
-- ==========================================

SELECT
company_id,
ROUND(AVG(sales),2) AS avg_sales
FROM profitandloss
GROUP BY company_id
ORDER BY avg_sales DESC
LIMIT 10;

-- ==========================================
-- Query 10: Null Value Check
-- ==========================================

SELECT
COUNT(*) AS null_book_values
FROM companies
WHERE book_value IS NULL;
