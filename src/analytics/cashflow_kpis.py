"""
Cash Flow Intelligence Module
Sprint 5 - Day 31

Outputs
-------
output/cashflow_intelligence.xlsx
output/distress_alerts.csv
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from src.analytics.cagr import calculate_cagr

# ==========================================================
# Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = PROJECT_ROOT / "data" / "raw"
SUPPORT_DIR = PROJECT_ROOT / "data" / "supporting"
OUTPUT_DIR = PROJECT_ROOT / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

PL_FILE = RAW_DIR / "profitandloss.xlsx"
BS_FILE = RAW_DIR / "balancesheet.xlsx"
CF_FILE = RAW_DIR / "cashflow.xlsx"
COMPANY_FILE = RAW_DIR / "companies.xlsx"

RATIO_FILE = SUPPORT_DIR / "financial_ratios.xlsx"

OUTPUT_FILE = OUTPUT_DIR / "cashflow_intelligence.xlsx"
DISTRESS_FILE = OUTPUT_DIR / "distress_alerts.csv"

# ==========================================================
# Logging
# ==========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# ==========================================================
# Dataset Loaders
# ==========================================================


def load_profit_loss():
    return pd.read_excel(
        PL_FILE,
        header=1
    )


def load_cashflow():
    return pd.read_excel(
        CF_FILE,
        header=1
    )


def load_balance_sheet():
    return pd.read_excel(
        BS_FILE,
        header=1
    )


def load_companies():
    return pd.read_excel(
        COMPANY_FILE,
        header=1
    )


def load_ratios():
    return pd.read_excel(
        RATIO_FILE
    )

# ==========================================================
# Helpers
# ==========================================================


def clean_year(df):

    df = df.copy()

    df["year"] = (
        df["year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
    )

    df = df.dropna(
        subset=["year"]
    )

    df["year"] = (
        df["year"]
        .astype(int)
    )

    return df.sort_values(
        "year"
    )


def latest(df):

    if df.empty:
        return None

    return df.iloc[-1]


def last_n(df, n):

    if len(df) < n:
        return pd.DataFrame()

    return df.tail(n)


def safe_divide(a, b):

    if pd.isna(a):
        return None

    if pd.isna(b):
        return None

    if b == 0:
        return None

    return a / b


def compute_cagr(
    df,
    column,
    years=5,
):

    if df.empty:
        return None

    df = df.sort_values(
        "year"
    )

    latest_row = df.iloc[-1]

    target_year = (
        latest_row["year"]
        - years
    )

    history = df[
        df.year <= target_year
    ]

    if history.empty:
        return None

    oldest = history.iloc[-1]

    value, status = calculate_cagr(

        oldest[column],

        latest_row[column],

        years,

        years,

    )

    if status != "OK":
        return None

    return round(value, 2)

# ==========================================================
# KPI Calculations
# ==========================================================


def calculate_free_cash_flow(
    operating_activity,
    investing_activity,
):
    """
    FCF = CFO + CFI

    Investing activity is already
    negative in the dataset.
    """

    return round(

        operating_activity
        + investing_activity,

        2,

    )


def calculate_cfo_quality_score(
    cfo,
    pat,
):

    if pat == 0:
        return None, None

    ratio = round(
        cfo / pat,
        2,
    )

    if ratio > 1:

        label = "High Quality"

    elif ratio >= 0.5:

        label = "Moderate"

    else:

        label = "Accrual Risk"

    return ratio, label


def calculate_capex_intensity(
    investing_activity,
    sales,
):

    if sales == 0:
        return None, None

    intensity = round(

        abs(investing_activity)

        / sales

        * 100,

        2,

    )

    if intensity < 3:

        label = "Asset Light"

    elif intensity <= 8:

        label = "Moderate"

    else:

        label = "Capital Intensive"

    return intensity, label

# ==========================================================
# Snapshot Builder
# ==========================================================


def get_company_snapshot(
    company_id,
    pl,
    cf,
    bs,
    ratios,
):

    return {

        "pl": clean_year(
            pl[
                pl.company_id == company_id
            ]
        ),

        "cf": clean_year(
            cf[
                cf.company_id == company_id
            ]
        ),

        "bs": clean_year(
            bs[
                bs.company_id == company_id
            ]
        ),

        "ratios": clean_year(
            ratios[
                ratios.company_id == company_id
            ]
        )

    }


# ==========================================================
# FCF Conversion
# ==========================================================


def calculate_fcf_conversion(
    free_cash_flow,
    net_profit,
):

    if net_profit == 0:
        return None

    return round(

        free_cash_flow

        /

        net_profit

        * 100,

        2,

    )


# ==========================================================
# Capital Allocation Classifier
# ==========================================================


def classify_capital_allocation(

    cfo,

    cfi,

    cff,

    cfo_quality=None,

):

    cfo_sign = "+" if cfo >= 0 else "-"

    cfi_sign = "+" if cfi >= 0 else "-"

    cff_sign = "+" if cff >= 0 else "-"

    pattern = (

        cfo_sign,

        cfi_sign,

        cff_sign,

    )

    if pattern == ("+", "-", "-"):

        if (

            cfo_quality is not None

            and

            cfo_quality > 1

        ):

            label = "Shareholder Returns"

        else:

            label = "Reinvestor"

    elif pattern == ("+", "+", "-"):

        label = "Liquidating Assets"

    elif pattern == ("-", "+", "+"):

        label = "Distress Signal"

    elif pattern == ("-", "-", "+"):

        label = "Growth Funded by Debt"

    elif pattern == ("+", "+", "+"):

        label = "Cash Accumulator"

    elif pattern == ("-", "-", "-"):

        label = "Pre-Revenue"

    elif pattern == ("+", "-", "+"):

        label = "Mixed"

    else:

        label = "Other"

    return label


# ==========================================================
# Average CFO Quality (5 Years)
# ==========================================================


def average_cfo_quality(snapshot):

    merged = pd.merge(

        snapshot["cf"],

        snapshot["pl"][

            [

                "year",

                "net_profit",

            ]

        ],

        on="year",

        how="inner",

    )

    merged = merged.tail(5)

    if merged.empty:

        return None, None

    scores = []

    for _, row in merged.iterrows():

        score, _ = calculate_cfo_quality_score(

            row["operating_activity"],

            row["net_profit"],

        )

        if score is not None:

            scores.append(score)

    if len(scores) == 0:

        return None, None

    average = round(

        sum(scores)

        /

        len(scores),

        2,

    )

    if average > 1:

        label = "High Quality"

    elif average >= 0.5:

        label = "Moderate"

    else:

        label = "Accrual Risk"

    return average, label


# ==========================================================
# FCF CAGR
# ==========================================================


def calculate_fcf_cagr(snapshot):

    merged = pd.merge(

        snapshot["cf"],

        snapshot["pl"][

            [

                "year",

                "sales",

            ]

        ],

        on="year",

        how="inner",

    )

    if len(merged) < 6:

        return None

    merged["fcf"] = (

        merged["operating_activity"]

        +

        merged["investing_activity"]

    )

    oldest = merged.iloc[-6]

    latest_row = merged.iloc[-1]

    value, status = calculate_cagr(

        oldest["fcf"],

        latest_row["fcf"],

        5,

        5,

    )

    if status != "OK":

        return None

    return round(

        value,

        2,

    )


# ==========================================================
# Distress Detection
# ==========================================================


def detect_distress(snapshot):

    latest_cf = latest(

        snapshot["cf"]

    )

    latest_pl = latest(

        snapshot["pl"]

    )

    if (

        latest_cf is None

        or

        latest_pl is None

    ):

        return False, None

    distressed = (

        latest_cf["operating_activity"] < 0

        and

        latest_cf["financing_activity"] > 0

    )

    details = {

        "cfo": latest_cf["operating_activity"],

        "cff": latest_cf["financing_activity"],

        "net_profit": latest_pl["net_profit"],

    }

    return distressed, details


# ==========================================================
# Deleveraging Detection
# ==========================================================


def detect_deleveraging(snapshot):

    cf = last_n(

        snapshot["cf"],

        2,

    )

    bs = last_n(

        snapshot["bs"],

        2,

    )

    if (

        cf.empty

        or

        bs.empty

    ):

        return False

    latest_cf = cf.iloc[-1]

    previous_bs = bs.iloc[-2]

    latest_bs = bs.iloc[-1]

    return (

        latest_cf["financing_activity"] < 0

        and

        latest_bs["borrowings"]

        <

        previous_bs["borrowings"]

    )

# ==========================================================
# Generate Intelligence
# ==========================================================


def generate_cashflow_intelligence():

    logger.info("Loading datasets...")

    companies = load_companies()
    pl = load_profit_loss()
    cf = load_cashflow()
    bs = load_balance_sheet()
    ratios = load_ratios()

    rows = []
    distress_rows = []

    logger.info("Processing companies...")

    for _, company in companies.iterrows():

        company_id = company["id"]
        company_name = company["company_name"]

        snapshot = get_company_snapshot(
            company_id,
            pl,
            cf,
            bs,
            ratios,
        )

        latest_pl = latest(snapshot["pl"])
        latest_cf = latest(snapshot["cf"])

        if latest_pl is None or latest_cf is None:

            logger.warning(
                "Skipping %s - missing Profit & Loss or Cash Flow data.",
                company_id,
            )

            continue

        # -----------------------------------
        # CFO Quality
        # -----------------------------------

        cfo_quality_score, cfo_quality_label = (
            average_cfo_quality(snapshot)
        )

        # -----------------------------------
        # CapEx Intensity
        # -----------------------------------

        capex_pct, capex_label = calculate_capex_intensity(
            latest_cf["investing_activity"],
            latest_pl["sales"],
        )

        # -----------------------------------
        # Free Cash Flow
        # -----------------------------------

        free_cash_flow = calculate_free_cash_flow(
            latest_cf["operating_activity"],
            latest_cf["investing_activity"],
        )

        # -----------------------------------
        # FCF CAGR
        # -----------------------------------

        fcf_cagr = calculate_fcf_cagr(snapshot)

        # -----------------------------------
        # FCF Conversion
        # -----------------------------------

        fcf_conversion = calculate_fcf_conversion(
            free_cash_flow,
            latest_pl["net_profit"],
        )

        # -----------------------------------
        # Distress
        # -----------------------------------

        distress_flag, distress_details = detect_distress(
            snapshot
        )

        # -----------------------------------
        # Deleveraging
        # -----------------------------------

        deleveraging_flag = detect_deleveraging(
            snapshot
        )

        # -----------------------------------
        # Capital Allocation
        # -----------------------------------

        capital_label = classify_capital_allocation(
            latest_cf["operating_activity"],
            latest_cf["investing_activity"],
            latest_cf["financing_activity"],
            cfo_quality_score,
        )

        # -----------------------------------
        # Sector
        # -----------------------------------

        sector = None

        if "sector" in company.index:
            sector = company["sector"]

        # -----------------------------------
        # Final Output Row
        # -----------------------------------

        rows.append(
            {
                "company_id": company_id,
                "company_name": company_name,
                "sector": sector,
                "cfo_quality_score": cfo_quality_score,
                "cfo_quality_label": cfo_quality_label,
                "capex_intensity_pct": capex_pct,
                "capex_label": capex_label,
                "fcf_cagr_5yr": fcf_cagr,
                "fcf_conversion_pct": fcf_conversion,
                "distress_flag": distress_flag,
                "deleveraging_flag": deleveraging_flag,
                "capital_allocation_label": capital_label,
            }
        )

        if distress_flag:

            distress_rows.append(
                {
                    "company_id": company_id,
                    "company_name": company_name,
                    "cfo": distress_details["cfo"],
                    "cff": distress_details["cff"],
                    "latest_net_profit": distress_details["net_profit"],
                }
            )

    intelligence_df = pd.DataFrame(rows)

    distress_df = pd.DataFrame(distress_rows)

    logger.info("Writing Excel...")

    intelligence_df.to_excel(
        OUTPUT_FILE,
        index=False,
    )

    logger.info("Writing Distress CSV...")

    distress_df.to_csv(
        DISTRESS_FILE,
        index=False,
    )

    logger.info("--------------------------------")

    logger.info(
        "Companies Processed : %d",
        len(intelligence_df),
    )

    logger.info(
        "Distress Alerts     : %d",
        len(distress_df),
    )

    logger.info(
        "Excel Output        : %s",
        OUTPUT_FILE,
    )

    logger.info(
        "CSV Output          : %s",
        DISTRESS_FILE,
    )

    logger.info("--------------------------------")


# ==========================================================
# Main
# ==========================================================


def main():

    generate_cashflow_intelligence()


if __name__ == "__main__":

    main()


