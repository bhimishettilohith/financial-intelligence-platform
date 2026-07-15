"""
Financial Ratio Calculations
Sprint 2 - Day 08
"""


def calculate_net_profit_margin(
    net_profit,
    sales
):
    """
    Net Profit Margin =
    net_profit / sales * 100
    """

    if sales == 0:
        return None

    return round(
        (net_profit / sales) * 100,
        2
    )


def calculate_operating_profit_margin(
    operating_profit,
    sales
):
    """
    Operating Profit Margin =
    operating_profit / sales * 100
    """

    if sales == 0:
        return None

    return round(
        (operating_profit / sales) * 100,
        2
    )


def calculate_roe(
    net_profit,
    equity_capital,
    reserves
):
    """
    Return on Equity
    """

    equity = (
        equity_capital +
        reserves
    )

    if equity <= 0:
        return None

    return round(
        (net_profit / equity) * 100,
        2
    )


def calculate_roce(
    operating_profit,
    other_income,
    equity_capital,
    reserves,
    borrowings
):
    """
    Return on Capital Employed
    """

    capital_employed = (
        equity_capital +
        reserves +
        borrowings
    )

    if capital_employed <= 0:
        return None

    ebit = (
        operating_profit +
        other_income
    )

    return round(
        (ebit / capital_employed) * 100,
        2
    )


def calculate_roa(
    net_profit,
    total_assets
):
    """
    Return on Assets
    """

    if total_assets == 0:
        return None

    return round(
        (net_profit / total_assets) * 100,
        2
    )

def calculate_debt_to_equity(
    borrowings,
    equity_capital,
    reserves
):
    """
    Debt to Equity Ratio
    """

    if borrowings == 0:
        return 0

    equity = (
        equity_capital +
        reserves
    )

    if equity <= 0:
        return None

    return round(
        borrowings / equity,
        2
    )

def calculate_high_leverage_flag(
    debt_to_equity,
    broad_sector
):
    """
    High leverage warning
    """

    if debt_to_equity is None:
        return False

    if broad_sector == "Financials":
        return False

    return debt_to_equity > 5

def calculate_interest_coverage(
    operating_profit,
    other_income,
    interest
):
    """
    Interest Coverage Ratio
    """

    if interest == 0:
        return None

    earnings = (
        operating_profit +
        other_income
    )

    return round(
        earnings / interest,
        2
    )

def calculate_icr_label(
    icr
):
    """
    Display label for ICR
    """

    if icr is None:
        return "Debt Free"

    return ""


def calculate_icr_warning_flag(
    icr
):
    """
    Interest coverage risk
    """

    if icr is None:
        return False

    return icr < 1.5


def calculate_net_debt(
    borrowings,
    investments
):
    """
    Net Debt
    """

    return round(
        borrowings -
        investments,
        2
    )


def calculate_asset_turnover(
    sales,
    total_assets
):
    """
    Asset Turnover Ratio
    """

    if total_assets == 0:
        return None

    return round(
        sales /
        total_assets,
        2
    )

