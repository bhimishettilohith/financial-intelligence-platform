from pathlib import Path
import sqlite3
import pandas as pd


DB_PATH = Path("nifty100.db")
SCHEMA_PATH = Path("db/schema.sql")

RAW_PATH = Path("data/raw")
SUPP_PATH = Path("data/supporting")


# ==========================================
# Database Creation
# ==========================================

def create_database():

    conn = sqlite3.connect(DB_PATH)

    conn.execute(
        "PRAGMA foreign_keys = ON;"
    )

    with open(
        SCHEMA_PATH,
        "r",
        encoding="utf-8"
    ) as f:

        conn.executescript(
            f.read()
        )

    return conn


# ==========================================
# Excel Loaders
# ==========================================

def load_core_file(file_name):

    return pd.read_excel(
        RAW_PATH / file_name,
        header=1
    )


def load_supporting_file(file_name):

    return pd.read_excel(
        SUPP_PATH / file_name
    )


# ==========================================
# FK Cleaner
# ==========================================

def filter_valid_company_ids(
    df,
    valid_company_ids
):

    if "company_id" not in df.columns:
        return df

    return df[
        df["company_id"].isin(
            valid_company_ids
        )
    ].copy()


# ==========================================
# Generic Table Loader
# ==========================================

def load_table(
    conn,
    table_name,
    df
):

    print(
        f"Loading {table_name}..."
    )

    df.to_sql(
        table_name,
        conn,
        if_exists="append",
        index=False
    )

    print(
        f"Rows Loaded: {len(df)}"
    )


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    print(
        "\nCreating SQLite database..."
    )

    conn = create_database()

    # --------------------------------------
    # Companies First
    # --------------------------------------

    companies = load_core_file(
        "companies.xlsx"
    )

    load_table(
        conn,
        "companies",
        companies
    )

    valid_company_ids = set(
        companies["id"]
    )

    # --------------------------------------
    # Core Tables
    # --------------------------------------

    profitandloss = filter_valid_company_ids(
        load_core_file(
            "profitandloss.xlsx"
        ),
        valid_company_ids
    )

    balancesheet = filter_valid_company_ids(
        load_core_file(
            "balancesheet.xlsx"
        ),
        valid_company_ids
    )

    cashflow = filter_valid_company_ids(
        load_core_file(
            "cashflow.xlsx"
        ),
        valid_company_ids
    )

    analysis = filter_valid_company_ids(
        load_core_file(
            "analysis.xlsx"
        ),
        valid_company_ids
    )

    documents = filter_valid_company_ids(
        load_core_file(
            "documents.xlsx"
        ),
        valid_company_ids
    )

    prosandcons = filter_valid_company_ids(
        load_core_file(
            "prosandcons.xlsx"
        ),
        valid_company_ids
    )

    # --------------------------------------
    # Supporting Tables
    # --------------------------------------

    financial_ratios = filter_valid_company_ids(
        load_supporting_file(
            "financial_ratios.xlsx"
        ),
        valid_company_ids
    )

    stock_prices = filter_valid_company_ids(
        load_supporting_file(
            "stock_prices.xlsx"
        ),
        valid_company_ids
    )

    sectors = filter_valid_company_ids(
        load_supporting_file(
            "sectors.xlsx"
        ),
        valid_company_ids
    )

    peer_groups = filter_valid_company_ids(
        load_supporting_file(
            "peer_groups.xlsx"
        ),
        valid_company_ids
    )

    # --------------------------------------
    # Load Tables
    # --------------------------------------

    load_table(
        conn,
        "profitandloss",
        profitandloss
    )

    load_table(
        conn,
        "balancesheet",
        balancesheet
    )

    load_table(
        conn,
        "cashflow",
        cashflow
    )

    load_table(
        conn,
        "analysis",
        analysis
    )

    load_table(
        conn,
        "documents",
        documents
    )

    load_table(
        conn,
        "prosandcons",
        prosandcons
    )

    load_table(
        conn,
        "financial_ratios",
        financial_ratios
    )

    load_table(
        conn,
        "stock_prices",
        stock_prices
    )

    load_table(
        conn,
        "sectors",
        sectors
    )

    load_table(
        conn,
        "peer_groups",
        peer_groups
    )

    conn.commit()

    print(
        "\nDatabase load completed successfully."
    )

    conn.close()    