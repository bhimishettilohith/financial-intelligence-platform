from src.analytics.cagr import (
    calculate_cagr
)


# =====================================
# Normal CAGR
# =====================================

def test_normal_cagr():

    value, flag = calculate_cagr(
        100,
        200,
        5
    )

    assert value == 14.87
    assert flag == "OK"


# =====================================
# Positive -> Negative
# =====================================

def test_decline_to_loss():

    value, flag = calculate_cagr(
        100,
        -50,
        5
    )

    assert value is None
    assert flag == "DECLINE_TO_LOSS"


# =====================================
# Negative -> Positive
# =====================================

def test_turnaround():

    value, flag = calculate_cagr(
        -100,
        50,
        5
    )

    assert value is None
    assert flag == "TURNAROUND"


# =====================================
# Negative -> Negative
# =====================================

def test_both_negative():

    value, flag = calculate_cagr(
        -100,
        -50,
        5
    )

    assert value is None
    assert flag == "BOTH_NEGATIVE"


# =====================================
# Zero Base
# =====================================

def test_zero_base():

    value, flag = calculate_cagr(
        0,
        100,
        5
    )

    assert value is None
    assert flag == "ZERO_BASE"


# =====================================
# Insufficient Data
# =====================================

def test_insufficient_data():

    value, flag = calculate_cagr(
        100,
        200,
        5,
        available_years=3
    )

    assert value is None
    assert flag == "INSUFFICIENT"


# =====================================
# 3-Year CAGR
# =====================================

def test_three_year_cagr():

    value, flag = calculate_cagr(
        100,
        150,
        3
    )

    assert flag == "OK"


# =====================================
# 5-Year CAGR
# =====================================

def test_five_year_cagr():

    value, flag = calculate_cagr(
        100,
        180,
        5
    )

    assert flag == "OK"


# =====================================
# 10-Year CAGR
# =====================================

def test_ten_year_cagr():

    value, flag = calculate_cagr(
        100,
        300,
        10
    )

    assert flag == "OK"


# =====================================
# Growth Exists
# =====================================

def test_positive_growth():

    value, flag = calculate_cagr(
        100,
        250,
        5
    )

    assert value > 0
    assert flag == "OK"