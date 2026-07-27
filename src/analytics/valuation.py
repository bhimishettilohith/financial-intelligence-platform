"""
Sprint 4 - Day 26
Valuation Module

Calculates:
- FCF Yield
- Company 5-Year Median PE
- Latest Sector Median PE
- Valuation Flags

Outputs:
output/valuation_summary.xlsx
output/valuation_flags.csv
"""

import os
import sqlite3
import logging
import numpy as np
import pandas as pd
from openpyxl import load_workbook

# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
)

DATABASE_PATH = os.path.join(
    BASE_DIR,
    "data",
    "nifty100.db"
)

MARKET_CAP_PATH = os.path.join(
    BASE_DIR,
    "data",
    "supporting",
    "market_cap.xlsx"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "output"
)

SUMMARY_FILE = os.path.join(
    OUTPUT_DIR,
    "valuation_summary.xlsx"
)

FLAGS_FILE = os.path.join(
    OUTPUT_DIR,
    "valuation_flags.csv"
)

CAUTION_THRESHOLD = 1.50
DISCOUNT_THRESHOLD = 0.70

os.makedirs(OUTPUT_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s : %(message)s"
)

# =============================================================================
# VALIDATION
# =============================================================================


def validate_inputs():

    if not os.path.exists(DATABASE_PATH):
        raise FileNotFoundError(
            f"Database not found:\n{DATABASE_PATH}"
        )

    if not os.path.exists(MARKET_CAP_PATH):
        raise FileNotFoundError(
            f"Market Cap file not found:\n{MARKET_CAP_PATH}"
        )


# =============================================================================
# DATABASE
# =============================================================================


def get_connection():
    return sqlite3.connect(DATABASE_PATH)


def run_query(query):

    conn = get_connection()

    try:
        df = pd.read_sql_query(query, conn)
    finally:
        conn.close()

    return df


# =============================================================================
# LOAD DATA
# =============================================================================


def load_market_cap():

    logging.info("Loading market_cap.xlsx")

    return pd.read_excel(MARKET_CAP_PATH)


def load_companies():

    query = """
    SELECT
        id AS company_id,
        company_name
    FROM companies
    """

    df = run_query(query)

    df = df.drop_duplicates(
        subset="company_id"
    )

    return df


def load_sectors():

    query = """
    SELECT
        company_id,
        broad_sector
    FROM sectors
    """

    df = run_query(query)

    df = df.drop_duplicates(
        subset="company_id"
    )

    return df


def load_cashflow():

    query = """
    SELECT
        company_id,
        year,
        operating_activity,
        investing_activity
    FROM cashflow
    """

    return run_query(query)


# =============================================================================
# YEAR UTILITIES
# =============================================================================


def extract_year(value):
    """
    Supports:

    2019
    2020
    Mar-13
    Mar-23
    Mar-2023
    """

    if pd.isna(value):
        return np.nan

    if isinstance(
        value,
        (
            int,
            float,
            np.integer,
            np.floating,
        )
    ):
        return int(value)

    value = str(value).strip()

    if value.isdigit():
        return int(value)

    if "-" in value:

        year = value.split("-")[-1]

        if year.isdigit():

            if len(year) == 2:

                year = int(year)

                if year >= 50:
                    return 1900 + year

                return 2000 + year

            return int(year)

    return np.nan


def latest_records(df):
    """
    Returns the latest record for each company.
    """

    temp = df.copy()

    temp["year_num"] = temp["year"].apply(extract_year)

    temp = temp.sort_values(
        ["company_id", "year_num"]
    )

    latest = (
        temp.groupby("company_id", as_index=False)
        .tail(1)
        .reset_index(drop=True)
    )

    return latest.drop(columns="year_num")


# =============================================================================
# FINANCIAL CALCULATIONS
# =============================================================================


def compute_fcf(cashflow):

    df = cashflow.copy()

    df["fcf"] = (
        df["operating_activity"]
        +
        df["investing_activity"]
    )

    return df


def compute_company_median_pe(
    market_cap
):

    median_df = (
        market_cap
        .groupby("company_id")["pe_ratio"]
        .median()
        .reset_index()
    )

    median_df.rename(
        columns={
            "pe_ratio": "median_pe_5yr"
        },
        inplace=True
    )

    return median_df


def compute_sector_median(
    latest_market,
    sectors
):

    temp = latest_market.merge(
        sectors,
        on="company_id",
        how="left"
    )

    sector = (
        temp
        .groupby("broad_sector")["pe_ratio"]
        .median()
        .reset_index()
    )

    sector.rename(
        columns={
            "pe_ratio": "sector_median_pe"
        },
        inplace=True
    )

    return sector

# =============================================================================
# DATA PREPARATION
# =============================================================================


def prepare_valuation_data():

    logging.info("Loading datasets...")

    market_cap = load_market_cap()
    companies = load_companies()
    sectors = load_sectors()
    cashflow = load_cashflow()

    logging.info("Preparing latest records...")

    latest_market = latest_records(market_cap)
    latest_cashflow = latest_records(cashflow)

    latest_cashflow = compute_fcf(latest_cashflow)

    company_median = compute_company_median_pe(
        market_cap
    )

    sector_median = compute_sector_median(
        latest_market,
        sectors
    )

    logging.info("Merging datasets...")

    df = latest_market.merge(
        companies,
        on="company_id",
        how="left"
    )

    df = df.merge(
        sectors,
        on="company_id",
        how="left"
    )

    df = df.merge(
        latest_cashflow[
            [
                "company_id",
                "fcf"
            ]
        ],
        on="company_id",
        how="left"
    )

    df = df.merge(
        company_median,
        on="company_id",
        how="left"
    )

    df = df.merge(
        sector_median,
        on="broad_sector",
        how="left"
    )

    return df


# =============================================================================
# METRIC CALCULATIONS
# =============================================================================


def compute_fcf_yield(df):

    df = df.copy()

    df["fcf_yield_pct"] = np.where(
        df["market_cap_crore"] > 0,
        (
            df["fcf"]
            /
            df["market_cap_crore"]
        )
        * 100,
        np.nan
    )

    return df


def compute_pe_vs_sector(df):

    df = df.copy()

    df["pe_vs_sector_median_pct"] = np.where(
        df["sector_median_pe"] > 0,
        (
            df["pe_ratio"]
            /
            df["sector_median_pe"]
        )
        * 100,
        np.nan
    )

    return df


def compute_premium_discount(df):

    df = df.copy()

    df["premium_discount_pct"] = np.where(
        df["sector_median_pe"] > 0,
        (
            (
                df["pe_ratio"]
                -
                df["sector_median_pe"]
            )
            /
            df["sector_median_pe"]
        )
        * 100,
        np.nan
    )

    return df


# =============================================================================
# FLAGGING
# =============================================================================


def assign_flag(row):

    pe = row["pe_ratio"]
    sector = row["sector_median_pe"]

    if pd.isna(pe) or pd.isna(sector):
        return "Unknown"

    if pe > sector * CAUTION_THRESHOLD:
        return "Caution"

    if pe < sector * DISCOUNT_THRESHOLD:
        return "Discount"

    return "Fair"


def compute_flags(df):

    df = df.copy()

    df["flag"] = df.apply(
        assign_flag,
        axis=1
    )

    return df


# =============================================================================
# SUMMARY TABLE
# =============================================================================


def create_summary(df):

    summary = df.copy()

    summary.rename(
        columns={
            "broad_sector": "sector"
        },
        inplace=True
    )

    summary = summary[
        [
            "company_id",
            "company_name",
            "sector",
            "year",
            "market_cap_crore",
            "fcf",
            "fcf_yield_pct",
            "pe_ratio",
            "median_pe_5yr",
            "sector_median_pe",
            "pe_vs_sector_median_pct",
            "premium_discount_pct",
            "pb_ratio",
            "ev_ebitda",
            "flag",
        ]
    ]

    summary.sort_values(
        [
            "flag",
            "fcf_yield_pct"
        ],
        ascending=[
            True,
            False
        ],
        inplace=True
    )

    summary.reset_index(
        drop=True,
        inplace=True
    )

    return summary

# =============================================================================
# EXPORT FUNCTIONS
# =============================================================================


def format_excel(file_path):
    """
    Apply basic formatting to the Excel workbook.
    """

    workbook = load_workbook(file_path)
    worksheet = workbook["Valuation"]

    # Freeze header row
    worksheet.freeze_panes = "A2"

    # Auto-adjust column widths
    for column_cells in worksheet.columns:

        max_length = 0
        column_letter = column_cells[0].column_letter

        for cell in column_cells:

            try:
                value = str(cell.value)

                if len(value) > max_length:
                    max_length = len(value)

            except Exception:
                pass

        worksheet.column_dimensions[
            column_letter
        ].width = max_length + 3

    workbook.save(file_path)


# =============================================================================
# EXPORT SUMMARY
# =============================================================================


def export_summary(summary):

    logging.info("Writing valuation_summary.xlsx")

    with pd.ExcelWriter(
        SUMMARY_FILE,
        engine="openpyxl"
    ) as writer:

        summary.to_excel(
            writer,
            index=False,
            sheet_name="Valuation"
        )

    format_excel(SUMMARY_FILE)


# =============================================================================
# EXPORT FLAGS
# =============================================================================


def export_flags(summary):

    logging.info("Writing valuation_flags.csv")

    flags = summary[
        summary["flag"].isin(
            [
                "Caution",
                "Discount"
            ]
        )
    ].copy()

    flags.to_csv(
        FLAGS_FILE,
        index=False
    )


# =============================================================================
# REPORTING
# =============================================================================


def print_summary(summary):

    print("\n")
    print("=" * 70)
    print("VALUATION SUMMARY")
    print("=" * 70)

    print(f"Companies Analysed : {len(summary)}")

    print(
        f"Caution Companies : "
        f"{(summary.flag == 'Caution').sum()}"
    )

    print(
        f"Discount Companies : "
        f"{(summary.flag == 'Discount').sum()}"
    )

    print(
        f"Fair Companies : "
        f"{(summary.flag == 'Fair').sum()}"
    )

    print(
        f"Unknown Companies : "
        f"{(summary.flag == 'Unknown').sum()}"
    )

    print("=" * 70)

    print("\nTop 10 Companies by FCF Yield\n")

    top10 = (
        summary.sort_values(
            "fcf_yield_pct",
            ascending=False
        )
        .head(10)
    )

    print(
        top10[
            [
                "company_name",
                "sector",
                "fcf_yield_pct",
                "flag"
            ]
        ].to_string(index=False)
    )

    print("\n")


# =============================================================================
# MAIN
# =============================================================================


def main():

    logging.info("=" * 70)
    logging.info("SPRINT 4 - DAY 26 : VALUATION MODULE")
    logging.info("=" * 70)

    try:

        # ------------------------------------------------------------------
        # Validate Inputs
        # ------------------------------------------------------------------

        validate_inputs()

        # ------------------------------------------------------------------
        # Prepare Data
        # ------------------------------------------------------------------

        df = prepare_valuation_data()

        # ------------------------------------------------------------------
        # Financial Metrics
        # ------------------------------------------------------------------

        logging.info("Computing FCF Yield...")
        df = compute_fcf_yield(df)

        logging.info("Computing PE vs Sector Median...")
        df = compute_pe_vs_sector(df)

        logging.info("Computing Premium / Discount...")
        df = compute_premium_discount(df)

        logging.info("Assigning Valuation Flags...")
        df = compute_flags(df)

        # ------------------------------------------------------------------
        # Create Summary
        # ------------------------------------------------------------------

        summary = create_summary(df)

        # ------------------------------------------------------------------
        # Round Numeric Columns
        # ------------------------------------------------------------------

        numeric_columns = [

            "market_cap_crore",
            "fcf",
            "fcf_yield_pct",
            "pe_ratio",
            "median_pe_5yr",
            "sector_median_pe",
            "pe_vs_sector_median_pct",
            "premium_discount_pct",
            "pb_ratio",
            "ev_ebitda",

        ]

        for column in numeric_columns:

            if column in summary.columns:

                summary[column] = summary[column].round(2)

        # ------------------------------------------------------------------
        # Export Files
        # ------------------------------------------------------------------

        export_summary(summary)

        export_flags(summary)

        # ------------------------------------------------------------------
        # Print Summary
        # ------------------------------------------------------------------

        print_summary(summary)

        logging.info("")
        logging.info("=" * 70)
        logging.info("VALUATION MODULE COMPLETED SUCCESSFULLY")
        logging.info("=" * 70)
        logging.info("")

        logging.info(f"Summary File : {SUMMARY_FILE}")
        logging.info(f"Flags File   : {FLAGS_FILE}")

    except Exception as e:

        logging.exception("Valuation Module Failed")

        raise e


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":

    main()