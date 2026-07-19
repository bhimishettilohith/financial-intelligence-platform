"""
Sprint 3 - Day 17
Composite Quality Score Engine
"""

from __future__ import annotations

import pandas as pd


# ----------------------------------------------------------
# Metric Configuration
# ----------------------------------------------------------

METRICS = {

    # ---------------- Profitability (35%) ----------------

    "return_on_equity_pct": {
        "weight": 15,
        "higher_is_better": True,
    },

    "return_on_capital_employed_pct": {
        "weight": 10,
        "higher_is_better": True,
    },

    "net_profit_margin_pct": {
        "weight": 10,
        "higher_is_better": True,
    },

    # ---------------- Cash Quality (30%) ----------------

    "free_cash_flow_cr": {
        "weight": 15,
        "higher_is_better": True,
    },

    "cfo_quality_score": {
        "weight": 10,
        "higher_is_better": True,
    },

    "fcf_positive_flag": {
        "weight": 5,
        "higher_is_better": True,
    },

    # ---------------- Growth (20%) ----------------

    "revenue_cagr_5yr": {
        "weight": 10,
        "higher_is_better": True,
    },

    "pat_cagr_5yr": {
        "weight": 10,
        "higher_is_better": True,
    },

    # ---------------- Leverage (15%) ----------------

    "debt_to_equity": {
        "weight": 10,
        "higher_is_better": False,
    },

    "interest_coverage": {
        "weight": 5,
        "higher_is_better": True,
    },
}


# ----------------------------------------------------------
# Winsorization
# ----------------------------------------------------------

def winsorize(series: pd.Series) -> pd.Series:
    """
    Cap values between the 10th and 90th percentile.
    """

    lower = series.quantile(0.10)
    upper = series.quantile(0.90)

    return series.clip(lower, upper)


# ----------------------------------------------------------
# Normalization
# ----------------------------------------------------------

def normalize(
    series: pd.Series,
    higher_is_better: bool = True,
) -> pd.Series:
    """
    Scale values to 0-100.
    """

    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:
        return pd.Series(
            50.0,
            index=series.index,
        )

    score = (
        (series - minimum)
        / (maximum - minimum)
    ) * 100

    if not higher_is_better:
        score = 100 - score

    return score


# ----------------------------------------------------------
# Score One Metric
# ----------------------------------------------------------

def score_metric(
    df: pd.DataFrame,
    column: str,
    higher_is_better: bool,
) -> pd.Series:

    values = winsorize(df[column])

    return normalize(
        values,
        higher_is_better,
    )


# ----------------------------------------------------------
# Generate FCF Flag
# ----------------------------------------------------------

def add_fcf_flag(
    df: pd.DataFrame,
) -> pd.DataFrame:

    df = df.copy()

    df["fcf_positive_flag"] = (
        df["free_cash_flow_cr"] > 0
    ).astype(int)

    return df
# ----------------------------------------------------------
# Composite Score
# ----------------------------------------------------------

def calculate_composite_score(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate the weighted composite quality score.

    - Uses only available metrics for each company.
    - Ignores missing metric values instead of producing NaN.
    - Returns a score between 0 and 100.
    """

    df = add_fcf_flag(df.copy())

    total_score = pd.Series(0.0, index=df.index)
    total_weight = pd.Series(0.0, index=df.index)

    for metric, config in METRICS.items():

        if metric not in df.columns:
            print(f"[INFO] Metric '{metric}' not found - skipped")
            continue

        scores = score_metric(
            df,
            metric,
            config["higher_is_better"],
        )

        # Rows where this metric exists
        valid_mask = df[metric].notna()

        # Missing metric contributes 0 points
        total_score += scores.fillna(0) * config["weight"]

        # Weight counted only when metric exists
        total_weight += valid_mask.astype(float) * config["weight"]

    # Avoid divide-by-zero
    total_weight = total_weight.replace(0, pd.NA)

    df["composite_quality_score"] = (
        total_score / total_weight
    ).round(2)

    return df

# ----------------------------------------------------------
# Sector Relative Score
# ----------------------------------------------------------

def calculate_sector_relative_score(
    df: pd.DataFrame,
    sector_column: str = "broad_sector",
) -> pd.DataFrame:
    """
    Normalize composite scores within each sector (0–100).
    """

    df = df.copy()

    if sector_column not in df.columns:
        raise ValueError(
            f"Column '{sector_column}' not found in DataFrame."
        )

    def normalize_sector(group: pd.DataFrame) -> pd.Series:

        scores = group["composite_quality_score"]

        minimum = scores.min()
        maximum = scores.max()

        if maximum == minimum:
            return pd.Series(
                50.0,
                index=group.index,
            )

        return (
            (scores - minimum)
            / (maximum - minimum)
        ) * 100

    df["sector_relative_score"] = (
        df.groupby(sector_column, group_keys=False)
          .apply(normalize_sector)
          .round(2)
    )

    return df