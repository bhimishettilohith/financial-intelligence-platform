"""
Capital Allocation Report
Sprint 5 - Day 32
"""

from pathlib import Path
import logging

import pandas as pd


# ------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = PROJECT_ROOT / "output"

CAPITAL_ALLOCATION_FILE = OUTPUT_DIR / "capital_allocation.csv"

CASHFLOW_INTELLIGENCE_FILE = (
    OUTPUT_DIR / "cashflow_intelligence.xlsx"
)

UPDATED_CASHFLOW_FILE = (
    OUTPUT_DIR / "cashflow_intelligence.xlsx"
)

DISTRIBUTION_FILE = (
    OUTPUT_DIR / "capital_allocation_distribution.csv"
)

PATTERN_CHANGES_FILE = (
    OUTPUT_DIR / "pattern_changes.csv"
)


# ------------------------------------------------------------------
# Load Data
# ------------------------------------------------------------------

def load_capital_allocation():

    logger.info("Loading capital allocation data...")

    return pd.read_csv(CAPITAL_ALLOCATION_FILE)


def load_cashflow_intelligence():

    logger.info("Loading cashflow intelligence...")

    return pd.read_excel(CASHFLOW_INTELLIGENCE_FILE)


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def clean_year(value):
    """
    Convert year values like:
    Mar 2023
    2023
    FY23
    into integer 2023
    """

    if pd.isna(value):
        return None

    text = str(value).strip()

    digits = "".join(ch for ch in text if ch.isdigit())

    if len(digits) >= 4:
        return int(digits[-4:])

    return None


def latest_year(df):

    years = df["year"].dropna().apply(clean_year)

    return years.max()


def previous_year(df):

    years = (
        sorted(
            df["year"]
            .dropna()
            .apply(clean_year)
            .unique()
        )
    )

    if len(years) < 2:
        return None

    return years[-2]


# ------------------------------------------------------------------
# Validation
# ------------------------------------------------------------------

def verify_capital_allocation(df):

    logger.info("Verifying capital allocation coverage...")

    coverage = (
        df.groupby("company_id")["year"]
        .nunique()
        .sort_values()
    )

    logger.info("--------------------------------")
    logger.info("Companies               : %s", len(coverage))
    logger.info("Minimum years available : %s", coverage.min())
    logger.info("Maximum years available : %s", coverage.max())
    logger.info("Average years available : %.2f", coverage.mean())
    logger.info("Coverage verification completed successfully.")
    logger.info("--------------------------------")

# ------------------------------------------------------------------
# Distribution Summary
# ------------------------------------------------------------------

def generate_distribution_summary(df):

    logger.info("Generating latest-year distribution...")

    latest = latest_year(df)

    latest_df = df[
        df["year"].apply(clean_year) == latest
    ].copy()

    # Detect the pattern column automatically
    pattern_column = None

    for column in latest_df.columns:

        name = column.lower().strip()

        if (
            "pattern" in name
            or "allocation" in name
            or "capital_allocation" in name
        ):
            pattern_column = column
            break

    if pattern_column is None:
        raise ValueError(
            "Could not locate capital allocation pattern column."
        )

    summary = (
        latest_df
        .groupby(pattern_column)
        .size()
        .reset_index(name="companies")
        .sort_values("companies", ascending=False)
    )

    summary.rename(
        columns={
            pattern_column: "capital_allocation"
        },
        inplace=True,
    )

    summary.to_csv(
        DISTRIBUTION_FILE,
        index=False,
    )

    logger.info(
        "Distribution summary written -> %s",
        DISTRIBUTION_FILE,
    )

    return latest_df, pattern_column


# ------------------------------------------------------------------
# Update Cashflow Intelligence
# ------------------------------------------------------------------

def update_cashflow_intelligence(
    cashflow_df,
    latest_patterns,
    pattern_column,
):

    logger.info(
        "Updating cashflow intelligence workbook..."
    )

    # Remove existing column if this script has already been run
    if "capital_allocation" in cashflow_df.columns:
        cashflow_df = cashflow_df.drop(
            columns=["capital_allocation"]
        )

    latest_mapping = (
        latest_patterns[
            ["company_id", pattern_column]
        ]
        .drop_duplicates(subset=["company_id"])
        .rename(
            columns={
                pattern_column: "capital_allocation"
            }
        )
    )

    updated = cashflow_df.merge(
        latest_mapping,
        on="company_id",
        how="left",
        validate="one_to_one",
    )

    updated.to_excel(
        UPDATED_CASHFLOW_FILE,
        index=False,
    )

    logger.info(
        "Updated workbook written -> %s",
        UPDATED_CASHFLOW_FILE,
    )

    return updated

# ------------------------------------------------------------------
# Pattern Changes
# ------------------------------------------------------------------

def generate_pattern_changes(df, pattern_column):

    logger.info("Detecting year-over-year pattern changes...")

    latest = latest_year(df)
    previous = previous_year(df)

    if previous is None:
        logger.warning("Previous year not found. Skipping pattern change report.")

        empty = pd.DataFrame(
            columns=[
                "company_id",
                "previous_year",
                "latest_year",
                "previous_pattern",
                "latest_pattern",
            ]
        )

        empty.to_csv(
            PATTERN_CHANGES_FILE,
            index=False,
        )

        return empty

    latest_df = df[
        df["year"].apply(clean_year) == latest
    ][["company_id", pattern_column]].rename(
        columns={
            pattern_column: "latest_pattern"
        }
    )

    previous_df = df[
        df["year"].apply(clean_year) == previous
    ][["company_id", pattern_column]].rename(
        columns={
            pattern_column: "previous_pattern"
        }
    )

    merged = latest_df.merge(
        previous_df,
        on="company_id",
        how="inner",
    )

    changes = merged[
        merged["latest_pattern"] != merged["previous_pattern"]
    ].copy()

    changes.insert(
        1,
        "previous_year",
        previous,
    )

    changes.insert(
        2,
        "latest_year",
        latest,
    )

    changes = changes[
        [
            "company_id",
            "previous_year",
            "latest_year",
            "previous_pattern",
            "latest_pattern",
        ]
    ]

    changes.to_csv(
        PATTERN_CHANGES_FILE,
        index=False,
    )

    logger.info(
        "Pattern changes written -> %s",
        PATTERN_CHANGES_FILE,
    )

    return changes


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------

def main():

    capital_df = load_capital_allocation()

    verify_capital_allocation(capital_df)

    cashflow_df = load_cashflow_intelligence()

    latest_patterns, pattern_column = (
        generate_distribution_summary(capital_df)
    )

    update_cashflow_intelligence(
        cashflow_df,
        latest_patterns,
        pattern_column,
    )

    changes = generate_pattern_changes(
        capital_df,
        pattern_column,
    )

    logger.info("--------------------------------")
    logger.info(
        "Companies : %s",
        capital_df["company_id"].nunique(),
    )
    logger.info(
        "Latest Year : %s",
        latest_year(capital_df),
    )
    logger.info(
        "Pattern Changes : %s",
        len(changes),
    )
    logger.info(
        "Distribution File : %s",
        DISTRIBUTION_FILE,
    )
    logger.info(
        "Pattern Report : %s",
        PATTERN_CHANGES_FILE,
    )
    logger.info("--------------------------------")


if __name__ == "__main__":
    main()

