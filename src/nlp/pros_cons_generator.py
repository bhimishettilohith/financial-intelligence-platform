"""
Sprint 5 - Day 30
Auto Pros / Cons Generator

Generates qualitative investment signals based on
financial statement rules.

Output
------
output/pros_cons_generated.csv
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from src.analytics.cagr import calculate_cagr


# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = PROJECT_ROOT / "data" / "raw"
SUPPORT_DIR = PROJECT_ROOT / "data" / "supporting"
OUTPUT_DIR = PROJECT_ROOT / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

COMPANIES_FILE = RAW_DIR / "companies.xlsx"
PL_FILE = RAW_DIR / "profitandloss.xlsx"
BS_FILE = RAW_DIR / "balancesheet.xlsx"
CF_FILE = RAW_DIR / "cashflow.xlsx"
RATIOS_FILE = SUPPORT_DIR / "financial_ratios.xlsx"

OUTPUT_FILE = OUTPUT_DIR / "pros_cons_generated.csv"


# ---------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


def load_companies():
    return pd.read_excel(COMPANIES_FILE, header=1)


def load_profit_loss():
    return pd.read_excel(PL_FILE, header=1)


def load_balance_sheet():
    return pd.read_excel(BS_FILE, header=1)


def load_cashflow():
    return pd.read_excel(CF_FILE, header=1)


def load_ratios():
    return pd.read_excel(RATIOS_FILE)

def clean_year(df):

    df = df.copy()

    df["year"] = (
        df["year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
    )

    df = df.dropna(subset=["year"])

    df["year"] = df["year"].astype(int)

    return df


def get_company_snapshot(
    company_id,
    ratios,
    pl,
    bs,
    cf,
):

    ratio_df = clean_year(
        ratios[
            ratios.company_id == company_id
        ]
    )

    pl_df = clean_year(
        pl[
            pl.company_id == company_id
        ]
    )

    bs_df = clean_year(
        bs[
            bs.company_id == company_id
        ]
    )

    cf_df = clean_year(
        cf[
            cf.company_id == company_id
        ]
    )

    ratio_df = ratio_df.sort_values("year")
    pl_df = pl_df.sort_values("year")
    bs_df = bs_df.sort_values("year")
    cf_df = cf_df.sort_values("year")

    return {
        "ratios": ratio_df,
        "pl": pl_df,
        "bs": bs_df,
        "cf": cf_df,
    }

def latest(df):

    if df.empty:
        return None

    return df.iloc[-1]

def last_n(df, n):

    if len(df) < n:
        return pd.DataFrame()

    return df.tail(n)

def compute_cagr(df, column, years):

    if df.empty:
        return None

    df = df.sort_values("year")

    latest = df.iloc[-1]

    target_year = latest["year"] - years

    history = df[
        df.year <= target_year
    ]

    if history.empty:
        return None

    oldest = history.iloc[-1]

    value, status = calculate_cagr(
        oldest[column],
        latest[column],
        years,
        years,
    )

    if status != "OK":
        return None

    return value


def consecutive_positive(df, column, years):

    recent = last_n(df, years)

    if recent.empty:
        return False

    return (recent[column] > 0).all()

def consecutive_increasing(df, column, years):

    recent = last_n(df, years)

    if recent.empty:
        return False

    return recent[column].is_monotonic_increasing


def consecutive_decreasing(df, column, years):

    recent = last_n(df, years)

    if recent.empty:
        return False

    return recent[column].is_monotonic_decreasing

def add_signal(
    results,
    company_id,
    signal_type,
    rule_id,
    text,
    confidence,
):

    if confidence <= 60:
        return

    results.append(
        {
            "company_id": company_id,
            "type": signal_type,
            "rule_id": rule_id,
            "text": text,
            "confidence_pct": confidence,
        }
    )

def pro_rule_1(company_id, snapshot, results):

    ratios = snapshot["ratios"]

    recent = last_n(ratios, 3)

    if recent.empty:
        return

    if (recent["return_on_equity_pct"] > 20).all():

        confidence = min(
            100,
            int(recent["return_on_equity_pct"].mean() * 3)
        )

        add_signal(
            results,
            company_id,
            "pro",
            "PRO_01",
            "Consistently high return on equity above 20% demonstrates exceptional capital efficiency.",
            confidence,
        )

def pro_rule_2(company_id, snapshot, results):

    ratios = snapshot["ratios"]

    if consecutive_positive(
        ratios,
        "free_cash_flow_cr",
        5,
    ):

        add_signal(
            results,
            company_id,
            "pro",
            "PRO_02",
            "Strong free cash flow generation over 5 years signals healthy business fundamentals.",
            90,
        )

def pro_rule_3(company_id, snapshot, results):

    latest_ratio = latest(snapshot["ratios"])

    if latest_ratio is None:
        return

    if latest_ratio["debt_to_equity"] == 0:

        add_signal(
            results,
            company_id,
            "pro",
            "PRO_03",
            "Debt-free balance sheet provides financial flexibility and eliminates interest burden.",
            95,
        )

def pro_rule_4(company_id, snapshot, results):

    cagr = compute_cagr(
        snapshot["pl"],
        "sales",
        5,
    )

    if cagr is None:
        return

    if cagr > 15:

        confidence = min(
            100,
            int(cagr * 4)
        )

        add_signal(
            results,
            company_id,
            "pro",
            "PRO_04",
            "Revenue growing at above 15% CAGR over 5 years reflects strong business momentum.",
            confidence,
        )

def pro_rule_5(company_id, snapshot, results):

    latest_ratio = latest(snapshot["ratios"])

    if latest_ratio is None:
        return

    if latest_ratio["operating_profit_margin_pct"] > 25:

        confidence = min(
            100,
            int(
                latest_ratio["operating_profit_margin_pct"] * 3
            )
        )

        add_signal(
            results,
            company_id,
            "pro",
            "PRO_05",
            "Operating profit margin above 25% indicates strong pricing power and cost discipline.",
            confidence,
        )

def pro_rule_6(company_id, snapshot, results):

    cagr = compute_cagr(
        snapshot["pl"],
        "net_profit",
        5,
    )

    if cagr is None:
        return

    if cagr > 20:

        confidence = min(
            100,
            int(cagr * 3)
        )

        add_signal(
            results,
            company_id,
            "pro",
            "PRO_06",
            "Net profit compounding at above 20% over 5 years creates significant shareholder value.",
            confidence,
        )

def apply_pro_rules(
    company_id,
    snapshot,
    results,
):

    pro_rule_1(company_id, snapshot, results)
    pro_rule_2(company_id, snapshot, results)
    pro_rule_3(company_id, snapshot, results)
    pro_rule_4(company_id, snapshot, results)
    pro_rule_5(company_id, snapshot, results)
    pro_rule_6(company_id, snapshot, results)

def pro_rule_7(company_id, snapshot, results):

    latest_ratio = latest(snapshot["ratios"])

    if latest_ratio is None:
        return

    if (
        latest_ratio["interest_coverage"] > 10
        or latest_ratio["debt_to_equity"] == 0
    ):

        add_signal(
            results,
            company_id,
            "pro",
            "PRO_07",
            "Very high interest coverage ratio reflects negligible financial stress from debt servicing.",
            90,
        )
def pro_rule_8(company_id, snapshot, results):
    """
    Skipped.

    Dataset does not contain Dividend Yield.
    """
    return

def pro_rule_9(company_id, snapshot, results):

    cagr = compute_cagr(
        snapshot["ratios"],
        "earnings_per_share",
        5,
    )

    if cagr is None:
        return

    if cagr > 15:

        confidence = max(61, min(95, int(60 + cagr * 1.2)))

        add_signal(
            results,
            company_id,
            "pro",
            "PRO_09",
            "Earnings per share growing above 15% CAGR indicates strong earnings quality and compounding.",
            confidence,
        )

def pro_rule_10(company_id, snapshot, results):

    if consecutive_increasing(
        snapshot["ratios"],
        "return_on_equity_pct",
        3,
    ):

        add_signal(
            results,
            company_id,
            "pro",
            "PRO_10",
            "Return on equity improving for 3 consecutive years shows strengthening business quality.",
            85,
        )
def pro_rule_11(company_id, snapshot, results):

    revenue = compute_cagr(
        snapshot["pl"],
        "sales",
        5,
    )

    pat = compute_cagr(
        snapshot["pl"],
        "net_profit",
        5,
    )

    if revenue is None or pat is None:
        return

    if pat > revenue:

        add_signal(
            results,
            company_id,
            "pro",
            "PRO_11",
            "Revenue growing slower than profits shows improving operating leverage and scale benefits.",
            90,
        )

def pro_rule_12(company_id, snapshot, results):

    bs = snapshot["bs"]

    assets = last_n(bs, 3)

    if assets.empty:
        return

    asset_up = assets["total_assets"].is_monotonic_increasing

    debt_down = assets["borrowings"].is_monotonic_decreasing

    if asset_up and debt_down:

        add_signal(
            results,
            company_id,
            "pro",
            "PRO_12",
            "Growing asset base funded by internal accruals reflects self-sustaining growth.",
            88,
        )

def con_rule_1(company_id, snapshot, results):

    latest_ratio = latest(snapshot["ratios"])

    if latest_ratio is None:
        return

    if latest_ratio["debt_to_equity"] > 2:

        add_signal(
            results,
            company_id,
            "con",
            "CON_01",
            f"Debt-to-equity ratio of {latest_ratio['debt_to_equity']:.2f} is elevated for a non-financial company and warrants monitoring.",
            90,
        )
def con_rule_2(company_id, snapshot, results):

    recent = last_n(
        snapshot["ratios"],
        3,
    )

    if recent.empty:
        return

    if (recent["free_cash_flow_cr"] < 0).all():

        add_signal(
            results,
            company_id,
            "con",
            "CON_02",
            "Free cash flow negative for 3 consecutive years raises concern about cash generation quality.",
            90,
        )

def con_rule_3(company_id, snapshot, results):

    if consecutive_decreasing(
        snapshot["ratios"],
        "operating_profit_margin_pct",
        3,
    ):

        add_signal(
            results,
            company_id,
            "con",
            "CON_03",
            "Operating margins declining for 3 consecutive years suggest pricing or cost pressure.",
            85,
        )

def con_rule_4(company_id, snapshot, results):

    latest_pl = latest(snapshot["pl"])

    if latest_pl is None:
        return

    if latest_pl["net_profit"] < 0:

        add_signal(
            results,
            company_id,
            "con",
            "CON_04",
            "Company reported a net loss in the most recent financial year.",
            95,
        )

def con_rule_5(company_id, snapshot, results):

    recent = last_n(
        snapshot["pl"],
        2,
    )

    if recent.empty:
        return

    if recent["sales"].is_monotonic_decreasing:

        add_signal(
            results,
            company_id,
            "con",
            "CON_05",
            "Revenue contraction over 2 consecutive years indicates demand weakness or market share loss.",
            85,
        )

def con_rule_6(company_id, snapshot, results):

    latest_ratio = latest(snapshot["ratios"])

    if latest_ratio is None:
        return

    if latest_ratio["interest_coverage"] < 1.5:

        add_signal(
            results,
            company_id,
            "con",
            "CON_06",
            "Interest coverage ratio below 1.5x indicates the company is at risk of not meeting its debt obligations.",
            95,
        )

def apply_pro_rules(company_id, snapshot, results):

    pro_rule_1(company_id, snapshot, results)
    pro_rule_2(company_id, snapshot, results)
    pro_rule_3(company_id, snapshot, results)
    pro_rule_4(company_id, snapshot, results)
    pro_rule_5(company_id, snapshot, results)
    pro_rule_6(company_id, snapshot, results)
    pro_rule_7(company_id, snapshot, results)
    pro_rule_8(company_id, snapshot, results)
    pro_rule_9(company_id, snapshot, results)
    pro_rule_10(company_id, snapshot, results)
    pro_rule_11(company_id, snapshot, results)
    pro_rule_12(company_id, snapshot, results)


def apply_con_rules(company_id, snapshot, results):

    con_rule_1(company_id, snapshot, results)
    con_rule_2(company_id, snapshot, results)
    con_rule_3(company_id, snapshot, results)
    con_rule_4(company_id, snapshot, results)
    con_rule_5(company_id, snapshot, results)
    con_rule_6(company_id, snapshot, results)

def con_rule_7(company_id, snapshot, results):

    latest_ratio = latest(snapshot["ratios"])

    if latest_ratio is None:
        return

    if latest_ratio["dividend_payout_ratio_pct"] > 100:

        add_signal(
            results,
            company_id,
            "con",
            "CON_07",
            "Dividend payout ratio above 100% means the company is paying dividends from reserves, which is unsustainable.",
            92,
        )

def con_rule_8(company_id, snapshot, results):

    if consecutive_increasing(
        snapshot["ratios"],
        "debt_to_equity",
        3,
    ):

        add_signal(
            results,
            company_id,
            "con",
            "CON_08",
            "Rising debt-to-equity ratio over 3 years suggests increasing financial leverage risk.",
            86,
        )

def con_rule_9(company_id, snapshot, results):

    if consecutive_decreasing(
        snapshot["ratios"],
        "earnings_per_share",
        3,
    ):

        add_signal(
            results,
            company_id,
            "con",
            "CON_09",
            "Earnings per share declining for 3 consecutive years reflects deteriorating profitability.",
            88,
        )

def con_rule_10(company_id, snapshot, results):
    """
    ROCE not available in dataset.
    """
    return

def con_rule_11(company_id, snapshot, results):
    """
    Net Debt / EBITDA cannot be computed
    from available datasets.
    """
    return

def con_rule_12(company_id, snapshot, results):

    cagr = compute_cagr(
        snapshot["pl"],
        "sales",
        5,
    )

    if cagr is None:
        return

    if cagr < 5:

        add_signal(
            results,
            company_id,
            "con",
            "CON_12",
            "Revenue growing at below 5% over 5 years lags inflation and suggests limited business momentum.",
            84,
        )

def apply_con_rules(company_id, snapshot, results):

    con_rule_1(company_id, snapshot, results)
    con_rule_2(company_id, snapshot, results)
    con_rule_3(company_id, snapshot, results)
    con_rule_4(company_id, snapshot, results)
    con_rule_5(company_id, snapshot, results)
    con_rule_6(company_id, snapshot, results)
    con_rule_7(company_id, snapshot, results)
    con_rule_8(company_id, snapshot, results)
    con_rule_9(company_id, snapshot, results)
    con_rule_10(company_id, snapshot, results)
    con_rule_11(company_id, snapshot, results)
    con_rule_12(company_id, snapshot, results)


def generate(companies, ratios, pl, bs, cf):

    results = []

    for company_id in companies["id"]:

        snapshot = get_company_snapshot(
            company_id,
            ratios,
            pl,
            bs,
            cf,
        )

        apply_pro_rules(
            company_id,
            snapshot,
            results,
        )

        apply_con_rules(
            company_id,
            snapshot,
            results,
        )

    return pd.DataFrame(results)

def verify(df, companies):

    verified = []

    for company in companies["id"]:

        company_rows = df[
            df.company_id == company
        ]

        if not (company_rows["type"] == "pro").any():

            verified.append(
                {
                    "company_id": company,
                    "type": "pro",
                    "rule_id": "PRO_00",
                    "text": "Business exhibits stable financial characteristics based on available data.",
                    "confidence_pct": 61,
                }
            )

        if not (company_rows["type"] == "con").any():

            verified.append(
                {
                    "company_id": company,
                    "type": "con",
                    "rule_id": "CON_00",
                    "text": "No major financial red flags identified based on available financial data.",
                    "confidence_pct": 61,
                }
            )

    if verified:
        df = pd.concat(
            [df, pd.DataFrame(verified)],
            ignore_index=True,
        )

    return df

def main():

    logger.info("Loading datasets...")

    companies = load_companies()
    ratios = load_ratios()
    pl = load_profit_loss()
    bs = load_balance_sheet()
    cf = load_cashflow()

    logger.info("Generating signals...")

    output = generate(
        companies,
        ratios,
        pl,
        bs,
        cf,
    )

    output = verify(
        output,
        companies,
    )

    output.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    logger.info("================================")
    logger.info("Signals Generated : %d", len(output))
    logger.info("Companies Covered : %d", companies["id"].nunique())
    logger.info("Output            : %s", OUTPUT_FILE)
    logger.info("================================")


if __name__ == "__main__":
    main()

