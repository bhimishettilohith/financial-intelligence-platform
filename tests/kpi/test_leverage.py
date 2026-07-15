from src.analytics.ratios import (
    calculate_debt_to_equity,
    calculate_high_leverage_flag,
    calculate_interest_coverage,
    calculate_icr_label,
    calculate_icr_warning_flag,
    calculate_net_debt,
    calculate_asset_turnover
)


# =====================================
# Debt-to-Equity Tests
# =====================================

def test_debt_to_equity_normal():

    assert (
        calculate_debt_to_equity(
            1000,
            200,
            800
        )
        == 1.0
    )


def test_debt_to_equity_debt_free():

    assert (
        calculate_debt_to_equity(
            0,
            200,
            800
        )
        == 0
    )


def test_debt_to_equity_negative_equity():

    assert (
        calculate_debt_to_equity(
            1000,
            -500,
            100
        )
        is None
    )


# =====================================
# High Leverage Flag
# =====================================

def test_high_leverage_flag():

    assert (
        calculate_high_leverage_flag(
            8,
            "Industrials"
        )
        is True
    )


def test_high_leverage_financials():

    assert (
        calculate_high_leverage_flag(
            8,
            "Financials"
        )
        is False
    )


# =====================================
# Interest Coverage Ratio
# =====================================

def test_interest_coverage_normal():

    assert (
        calculate_interest_coverage(
            200,
            50,
            50
        )
        == 5.0
    )


def test_interest_coverage_zero_interest():

    assert (
        calculate_interest_coverage(
            200,
            50,
            0
        )
        is None
    )


# =====================================
# Debt Free Label
# =====================================

def test_icr_label_debt_free():

    assert (
        calculate_icr_label(
            None
        )
        == "Debt Free"
    )


# =====================================
# ICR Warning
# =====================================

def test_icr_warning_flag():

    assert (
        calculate_icr_warning_flag(
            1.2
        )
        is True
    )


# =====================================
# Net Debt
# =====================================

def test_net_debt():

    assert (
        calculate_net_debt(
            1000,
            300
        )
        == 700
    )


# =====================================
# Asset Turnover
# =====================================

def test_asset_turnover_zero_assets():

    assert (
        calculate_asset_turnover(
            1000,
            0
        )
        is None
    )