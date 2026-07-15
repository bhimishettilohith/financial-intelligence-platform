import math


def calculate_cagr(
    start_value,
    end_value,
    years,
    available_years=None
):
    """
    CAGR Calculation
    """

    if (
        available_years is not None
        and available_years < years
    ):
        return (
            None,
            "INSUFFICIENT"
        )

    if start_value == 0:
        return (
            None,
            "ZERO_BASE"
        )

    if start_value > 0 and end_value < 0:
        return (
            None,
            "DECLINE_TO_LOSS"
        )

    if start_value < 0 and end_value > 0:
        return (
            None,
            "TURNAROUND"
        )

    if start_value < 0 and end_value < 0:
        return (
            None,
            "BOTH_NEGATIVE"
        )

    cagr = (
        (
            end_value /
            start_value
        ) ** (1 / years)
        - 1
    ) * 100

    return (
        round(cagr, 2),
        "OK"
    )