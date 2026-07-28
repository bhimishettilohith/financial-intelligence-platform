import time

TICKERS = [
    "TCS",
    "INFY",
    "HCLTECH",
    "RELIANCE",
    "HDFCBANK",
]


def test_company_profile_speed(client):

    timings = {}

    for ticker in TICKERS:

        start = time.perf_counter()

        response = client.get(f"/api/v1/companies/{ticker}")

        elapsed = time.perf_counter() - start

        timings[ticker] = elapsed

        assert response.status_code == 200
        assert elapsed < 3

    print()

    for ticker, value in timings.items():
        print(f"{ticker}: {value:.3f}s")
