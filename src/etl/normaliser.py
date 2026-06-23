import re


def normalize_year(year):
    """
    Normalize year values to integer format.

    Examples:
    2024 -> 2024
    '2024' -> 2024
    'FY24' -> 2024
    'FY 2024' -> 2024
    """

    if year is None:
        return None

    year = str(year).strip().upper()

    year = year.replace("FY", "").strip()

    digits = re.findall(r"\d+", year)

    if not digits:
        return None

    value = digits[0]

    if len(value) == 2:
        return int("20" + value)

    return int(value)


def normalize_ticker(ticker):
    """
    Standardize stock tickers.

    Examples:
    'tcs'
    ' TCS '
    'tcs.ns'

    -> 'TCS'
    """

    if ticker is None:
        return None

    ticker = str(ticker).strip().upper()

    ticker = ticker.replace(".NS", "")
    ticker = ticker.replace(".BO", "")

    return ticker