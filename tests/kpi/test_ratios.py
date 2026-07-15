from src.analytics.ratios import (
    calculate_net_profit_margin,
    calculate_operating_profit_margin,
    calculate_roe,
    calculate_roce,
    calculate_roa
)


# =====================================
# NPM Tests
# =====================================

def test_net_profit_margin_normal():

    assert (
        calculate_net_profit_margin(
            100,
            1000
        )
        == 10.0
    )


def test_net_profit_margin_zero_sales():

    assert (
        calculate_net_profit_margin(
            100,
            0
        )
        is None
    )


# =====================================
# OPM Tests
# =====================================

def test_operating_profit_margin_normal():

    assert (
        calculate_operating_profit_margin(
            150,
            1000
        )
        == 15.0
    )


def test_opm_cross_check_mismatch():

    calculated = calculate_operating_profit_margin(
        150,
        1000
    )

    source_value = 12.0

    assert abs(
        calculated - source_value
    ) > 1


# =====================================
# ROE Tests
# =====================================

def test_roe_normal():

    assert (
        calculate_roe(
            100,
            200,
            300
        )
        == 20.0
    )


def test_roe_negative_equity():

    assert (
        calculate_roe(
            100,
            -200,
            100
        )
        is None
    )


# =====================================
# ROCE Tests
# =====================================

def test_roce_normal():

    assert (
        calculate_roce(
            operating_profit=150,
            other_income=50,
            equity_capital=500,
            reserves=500,
            borrowings=1000
        )
        == 10.0
    )


# =====================================
# ROA Tests
# =====================================

def test_roa_zero_assets():

    assert (
        calculate_roa(
            100,
            0
        )
        is None
    )