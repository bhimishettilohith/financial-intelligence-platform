from src.analytics.cashflow_kpis import (
    calculate_free_cash_flow,
    calculate_cfo_quality_score,
    calculate_capex_intensity,
    calculate_fcf_conversion,
    classify_capital_allocation
)


# =====================================
# Free Cash Flow
# =====================================

def test_free_cash_flow():

    assert (
        calculate_free_cash_flow(
            1000,
            -300
        )
        == 700
    )


# =====================================
# CFO Quality
# =====================================

def test_cfo_quality_high():

    ratio, label = (
        calculate_cfo_quality_score(
            1200,
            1000
        )
    )

    assert ratio == 1.2
    assert label == "High Quality"


def test_cfo_quality_moderate():

    ratio, label = (
        calculate_cfo_quality_score(
            700,
            1000
        )
    )

    assert ratio == 0.7
    assert label == "Moderate"


def test_cfo_quality_accrual_risk():

    ratio, label = (
        calculate_cfo_quality_score(
            300,
            1000
        )
    )

    assert ratio == 0.3
    assert label == "Accrual Risk"


def test_cfo_quality_pat_zero():

    ratio, label = (
        calculate_cfo_quality_score(
            1000,
            0
        )
    )

    assert ratio is None
    assert label is None


# =====================================
# CapEx Intensity
# =====================================

def test_capex_intensity_asset_light():

    value, label = (
        calculate_capex_intensity(
            -20,
            1000
        )
    )

    assert label == "Asset Light"


def test_capex_intensity_moderate():

    value, label = (
        calculate_capex_intensity(
            -50,
            1000
        )
    )

    assert label == "Moderate"


def test_capex_intensity_capital_intensive():

    value, label = (
        calculate_capex_intensity(
            -150,
            1000
        )
    )

    assert label == "Capital Intensive"


# =====================================
# FCF Conversion
# =====================================

def test_fcf_conversion():

    assert (
        calculate_fcf_conversion(
            700,
            1000
        )
        == 70.0
    )


def test_fcf_conversion_zero_op():

    assert (
        calculate_fcf_conversion(
            700,
            0
        )
        is None
    )


# =====================================
# Capital Allocation
# =====================================

def test_shareholder_returns():

    result = (
        classify_capital_allocation(
            1000,
            -500,
            -300,
            1.2
        )
    )

    assert (
        result["pattern_label"]
        ==
        "Shareholder Returns"
    )


def test_reinvestor():

    result = (
        classify_capital_allocation(
            1000,
            -500,
            -300,
            0.8
        )
    )

    assert (
        result["pattern_label"]
        ==
        "Reinvestor"
    )


def test_distress_signal():

    result = (
        classify_capital_allocation(
            -100,
            50,
            50
        )
    )

    assert (
        result["pattern_label"]
        ==
        "Distress Signal"
    )


def test_growth_funded_by_debt():

    result = (
        classify_capital_allocation(
            -100,
            -50,
            200
        )
    )

    assert (
        result["pattern_label"]
        ==
        "Growth Funded by Debt"
    )


def test_cash_accumulator():

    result = (
        classify_capital_allocation(
            100,
            50,
            25
        )
    )

    assert (
        result["pattern_label"]
        ==
        "Cash Accumulator"
    )