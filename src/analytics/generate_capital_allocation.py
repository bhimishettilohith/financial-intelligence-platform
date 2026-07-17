import sqlite3
import pandas as pd

from src.analytics.cashflow_kpis import (
    classify_capital_allocation
)


DB_PATH =  "data/nifty100.db"
OUTPUT_FILE = "output/capital_allocation.csv"


print("Loading database...")

conn = sqlite3.connect(DB_PATH)

cashflow = pd.read_sql(
    """
    SELECT *
    FROM cashflow
    """,
    conn
)

profitandloss = pd.read_sql(
    """
    SELECT
        company_id,
        year,
        net_profit
    FROM profitandloss
    """,
    conn
)

conn.close()

print("Preparing data...")

merged = cashflow.merge(
    profitandloss,
    on=["company_id", "year"],
    how="left"
)

results = []

print("Generating classifications...")

for _, row in merged.iterrows():

    cfo = row["operating_activity"]
    cfi = row["investing_activity"]
    cff = row["financing_activity"]

    pat = row["net_profit"]

    cfo_pat_ratio = None

    if (
        pd.notna(pat)
        and pat != 0
    ):
        cfo_pat_ratio = (
            cfo / pat
        )

    classification = (
        classify_capital_allocation(
            cfo,
            cfi,
            cff,
            cfo_pat_ratio
        )
    )

    results.append({
        "company_id": row["company_id"],
        "year": row["year"],
        "cfo_sign": classification["cfo_sign"],
        "cfi_sign": classification["cfi_sign"],
        "cff_sign": classification["cff_sign"],
        "pattern_label":
            classification["pattern_label"]
    })

capital_allocation = pd.DataFrame(
    results
)

capital_allocation.to_csv(
    OUTPUT_FILE,
    index=False
)

print(
    f"Generated {OUTPUT_FILE}"
)

print(
    f"Rows: {len(capital_allocation)}"
)

print("\nPattern Summary:")

print(
    capital_allocation[
        "pattern_label"
    ].value_counts()
)