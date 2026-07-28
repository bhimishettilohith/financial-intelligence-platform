"""
Sprint 6 - Day 43

Create performance indexes.
"""

import sqlite3

DB_PATH = "data/nifty100.db"

INDEXES = [
    # Profit & Loss
    "CREATE INDEX IF NOT EXISTS idx_pl_company ON profitandloss(company_id);",
    "CREATE INDEX IF NOT EXISTS idx_pl_year ON profitandloss(year);",
    "CREATE INDEX IF NOT EXISTS idx_pl_company_year ON profitandloss(company_id, year);",
    # Balance Sheet
    "CREATE INDEX IF NOT EXISTS idx_bs_company ON balancesheet(company_id);",
    "CREATE INDEX IF NOT EXISTS idx_bs_year ON balancesheet(year);",
    "CREATE INDEX IF NOT EXISTS idx_bs_company_year ON balancesheet(company_id, year);",
    # Cashflow
    "CREATE INDEX IF NOT EXISTS idx_cf_company ON cashflow(company_id);",
    "CREATE INDEX IF NOT EXISTS idx_cf_year ON cashflow(year);",
    "CREATE INDEX IF NOT EXISTS idx_cf_company_year ON cashflow(company_id, year);",
    # Financial Ratios
    "CREATE INDEX IF NOT EXISTS idx_fr_company_year ON financial_ratios(company_id, year);",
    # Computed Ratios
    "CREATE INDEX IF NOT EXISTS idx_cfr_company_year ON computed_financial_ratios(company_id, year);",
    # Stock Prices
    "CREATE INDEX IF NOT EXISTS idx_stock_company_date ON stock_prices(company_id, date);",
    # Peer Percentiles
    "CREATE INDEX IF NOT EXISTS idx_peer_company_year ON peer_percentiles(company_id, year);",
    # Documents
    "CREATE INDEX IF NOT EXISTS idx_documents_company_year ON documents(company_id, year);",
    # Sectors
    "CREATE INDEX IF NOT EXISTS idx_sector_company ON sectors(company_id);",
]

conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()

for sql in INDEXES:
    cursor.execute(sql)

conn.commit()

print("Indexes created successfully.")

conn.close()
