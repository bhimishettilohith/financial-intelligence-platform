"""
Cash Flow KPI Calculations
Sprint 2 - Day 11
"""


# =====================================
# Free Cash Flow
# =====================================

def calculate_free_cash_flow(
    operating_activity,
    investing_activity
):
    """
    FCF = CFO + CFI

    Note:
    investing_activity is already
    negative in the dataset.
    """

    return round(
        operating_activity +
        investing_activity,
        2
    )


# =====================================
# CFO Quality Score
# =====================================

def calculate_cfo_quality_score(
    cfo,
    pat
):
    """
    CFO / PAT

    >1.0      = High Quality
    0.5-1.0   = Moderate
    <0.5      = Accrual Risk
    """

    if pat == 0:
        return None, None

    ratio = round(
        cfo / pat,
        2
    )

    if ratio > 1:
        label = "High Quality"

    elif ratio >= 0.5:
        label = "Moderate"

    else:
        label = "Accrual Risk"

    return ratio, label


# =====================================
# CapEx Intensity
# =====================================

def calculate_capex_intensity(
    investing_activity,
    sales
):
    """
    abs(CFI) / Sales * 100

    <3%   = Asset Light
    3-8%  = Moderate
    >8%   = Capital Intensive
    """

    if sales == 0:
        return None, None

    intensity = round(
        abs(investing_activity)
        / sales
        * 100,
        2
    )

    if intensity < 3:
        label = "Asset Light"

    elif intensity <= 8:
        label = "Moderate"

    else:
        label = "Capital Intensive"

    return intensity, label


# =====================================
# FCF Conversion
# =====================================

def calculate_fcf_conversion(
    free_cash_flow,
    operating_profit
):
    """
    FCF / Operating Profit * 100
    """

    if operating_profit == 0:
        return None

    return round(
        free_cash_flow
        / operating_profit
        * 100,
        2
    )


# =====================================
# Capital Allocation Classifier
# =====================================

def classify_capital_allocation(
    cfo,
    cfi,
    cff,
    cfo_pat_ratio=None
):
    """
    Capital Allocation Pattern
    """

    cfo_sign = "+" if cfo >= 0 else "-"
    cfi_sign = "+" if cfi >= 0 else "-"
    cff_sign = "+" if cff >= 0 else "-"

    pattern = (
        cfo_sign,
        cfi_sign,
        cff_sign
    )

    if pattern == ("+", "-", "-"):

        if (
            cfo_pat_ratio is not None
            and cfo_pat_ratio > 1
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

    return {
        "cfo_sign": cfo_sign,
        "cfi_sign": cfi_sign,
        "cff_sign": cff_sign,
        "pattern_label": label
    }