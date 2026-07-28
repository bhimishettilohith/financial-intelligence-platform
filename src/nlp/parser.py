"""
Sprint 5 - Day 29
Analysis Text Parser

Parses CAGR-related text fields from analysis.xlsx into a
structured dataset and validates them against computed values.

Outputs
-------
output/analysis_parsed.csv
output/parse_failures.csv
output/cagr_validation.csv
"""

from __future__ import annotations

import logging
import re
from pathlib import Path

import pandas as pd

from src.analytics.cagr import calculate_cagr

# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = PROJECT_ROOT / "data" / "raw"
SUPPORTING_DIR = PROJECT_ROOT / "data" / "supporting"
OUTPUT_DIR = PROJECT_ROOT / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

ANALYSIS_FILE = RAW_DIR / "analysis.xlsx"
PL_FILE = RAW_DIR / "profitandloss.xlsx"
STOCK_FILE = SUPPORTING_DIR / "stock_prices.xlsx"

PARSED_FILE = OUTPUT_DIR / "analysis_parsed.csv"
FAILURE_FILE = OUTPUT_DIR / "parse_failures.csv"
VALIDATION_FILE = OUTPUT_DIR / "cagr_validation.csv"

# ---------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------
# Regex Pattern
# ---------------------------------------------------------------------

PATTERN = re.compile(
    r"(TTM|Last\s+Year|\d+\s*Years?)\s*:?\s*(-?[\d.]+)\s*%",
    re.IGNORECASE,
)

TARGET_FIELDS = [
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe",
]

# ---------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------


def load_analysis() -> pd.DataFrame:
    """
    Load analysis.xlsx
    """

    logger.info("Loading analysis.xlsx")

    return pd.read_excel(ANALYSIS_FILE, header=1)


def load_profit_loss() -> pd.DataFrame:
    """
    Load profitandloss.xlsx
    """

    logger.info("Loading profitandloss.xlsx")

    return pd.read_excel(PL_FILE, header=1)


def load_stock_prices() -> pd.DataFrame:
    """
    Load stock_prices.xlsx
    """

    logger.info("Loading stock_prices.xlsx")

    df = pd.read_excel(STOCK_FILE)

    df["date"] = pd.to_datetime(df["date"])

    return df


# ---------------------------------------------------------------------
# Parsing Helpers
# ---------------------------------------------------------------------


def parse_metric_text(text):
    """
    Parse text like:
        10 Years: 21%
        1 Year: -2%
        TTM: 43%
        Last Year: 12%
    """

    if pd.isna(text):
        return None, None

    text = str(text).strip()

    match = PATTERN.search(text)

    if not match:
        return None, None

    period_text = match.group(1).strip().lower()
    value = float(match.group(2))

    if period_text == "ttm":
        period = "TTM"
    elif period_text == "last year":
        period = "LAST_YEAR"
    else:
        period = int(re.search(r"\d+", period_text).group())

    return period, value


def parse_analysis(df):
    """
    Parse all target fields.

    Returns

    parsed_df
    failures_df
    """

    parsed_rows = []

    failures = []

    for _, row in df.iterrows():

        company_id = row["company_id"]

        for field in TARGET_FIELDS:

            period, value = parse_metric_text(row[field])

            if period is None:

                failures.append(
                    {
                        "company_id": company_id,
                        "metric_type": field,
                        "raw_text": row[field],
                        "reason": "REGEX_NOT_MATCHED",
                    }
                )

                continue

            parsed_rows.append(
                {
                    "company_id": company_id,
                    "metric_type": field,
                    "period_years": period,
                    "value_pct": value,
                }
            )

    parsed_df = pd.DataFrame(parsed_rows)

    failures_df = pd.DataFrame(failures)

    return parsed_df, failures_df


# ---------------------------------------------------------------------
# Validation Helpers
# ---------------------------------------------------------------------


def compute_profit_cagr(
    company_df: pd.DataFrame,
    value_column: str,
    years: int,
):
    """
    Compute CAGR using the existing Ratio Engine.
    """

    if company_df.empty:
        return None, "NO_DATA"

    company_df = company_df.copy()

    # Extract 4-digit year and remove rows like "TTM"
    company_df["year"] = company_df["year"].astype(str).str.extract(r"(\d{4})")[0]

    company_df = company_df.dropna(subset=["year"])

    company_df["year"] = company_df["year"].astype(int)

    company_df = company_df.sort_values("year")

    latest = company_df.iloc[-1]

    # Find the closest record at least 'years' years older
    target_year = latest["year"] - years

    historical = company_df[company_df["year"] <= target_year]

    if historical.empty:
        return None, "INSUFFICIENT_DATA"

    oldest = historical.iloc[-1]

    start = oldest[value_column]
    end = latest[value_column]

    if pd.isna(start) or pd.isna(end):
        return None, "MISSING_VALUE"

    if start == 0:
        return None, "ZERO_BASE"

    return calculate_cagr(
        start_value=start,
        end_value=end,
        years=years,
        available_years=years,
    )


def compute_stock_price_cagr(
    stock_df: pd.DataFrame,
    company_id,
    years,
):
    """
    Compute stock CAGR using adjusted close.
    """

    df = stock_df[stock_df["company_id"] == company_id].copy()

    if df.empty:
        return None, "NO_PRICE_DATA"

    df = df.sort_values("date")

    latest = df.iloc[-1]

    target_date = latest["date"] - pd.DateOffset(years=years)

    historical = df[df["date"] <= target_date]

    if historical.empty:
        return None, "INSUFFICIENT_DATA"

    oldest = historical.iloc[-1]

    return calculate_cagr(
        oldest["adjusted_close"],
        latest["adjusted_close"],
        years,
        years,
    )


# ---------------------------------------------------------------------
# Cross Validation
# ---------------------------------------------------------------------


def cross_validate(
    parsed_df,
    profit_loss_df,
    stock_df,
):
    """
    Compare parsed CAGR values against computed CAGR.
    """

    validations = []

    for _, row in parsed_df.iterrows():

        company_id = row["company_id"]

        metric = row["metric_type"]

        period = row["period_years"]

        if period in ("TTM", "LAST_YEAR"):
            validations.append(
                {
                    "company_id": company_id,
                    "metric_type": metric,
                    "period_years": period,
                    "parsed_pct": parsed_value,
                    "computed_pct": None,
                    "difference_pct": None,
                    "status": "NOT_APPLICABLE",
                }
            )
            continue

        years = int(period)

        parsed_value = row["value_pct"]

        computed = None

        status = "OK"

        if metric == "compounded_sales_growth":

            computed, status = compute_profit_cagr(
                profit_loss_df[profit_loss_df["company_id"] == company_id],
                "sales",
                years,
            )

        elif metric == "compounded_profit_growth":

            computed, status = compute_profit_cagr(
                profit_loss_df[profit_loss_df["company_id"] == company_id],
                "net_profit",
                years,
            )

        elif metric == "stock_price_cagr":

            computed, status = compute_stock_price_cagr(
                stock_df,
                company_id,
                years,
            )

        elif metric == "roe":

            status = "NOT_APPLICABLE"

        difference = None

        if computed is not None and status == "OK":
            difference = round(
                abs(parsed_value - computed),
                2,
            )

            if difference > 5:
                status = "DIVERGENCE"

        validations.append(
            {
                "company_id": company_id,
                "metric_type": metric,
                "period_years": years,
                "parsed_pct": parsed_value,
                "computed_pct": computed,
                "difference_pct": difference,
                "status": status,
            }
        )

    return pd.DataFrame(validations)


# ---------------------------------------------------------------------
# Save Helpers
# ---------------------------------------------------------------------


def save_outputs(
    parsed_df,
    failures_df,
    validation_df,
):

    parsed_df.to_csv(
        PARSED_FILE,
        index=False,
    )

    failures_df.to_csv(
        FAILURE_FILE,
        index=False,
    )

    validation_df.to_csv(
        VALIDATION_FILE,
        index=False,
    )

    logger.info(
        "Saved %s",
        PARSED_FILE,
    )

    logger.info(
        "Saved %s",
        FAILURE_FILE,
    )

    logger.info(
        "Saved %s",
        VALIDATION_FILE,
    )


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------


def main():

    analysis_df = load_analysis()

    profit_loss_df = load_profit_loss()

    stock_df = load_stock_prices()

    parsed_df, failures_df = parse_analysis(analysis_df)

    validation_df = cross_validate(
        parsed_df,
        profit_loss_df,
        stock_df,
    )

    save_outputs(
        parsed_df,
        failures_df,
        validation_df,
    )

    logger.info("========== SUMMARY ==========")

    logger.info(
        "Parsed Records : %d",
        len(parsed_df),
    )

    logger.info(
        "Failures       : %d",
        len(failures_df),
    )

    logger.info(
        "Validation Rows: %d",
        len(validation_df),
    )


if __name__ == "__main__":
    main()
