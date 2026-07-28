"""
Valuation Service
"""


class ValuationService:

    def __init__(self, conn):
        self.conn = conn

    def get_market_cap_history(self, ticker: str):

        return {
            "ticker": ticker,
            "available": False,
            "message": (
                "Historical valuation multiples "
                "(P/E, P/B, EV/EBITDA, Dividend Yield) "
                "are not available in the current dataset."
            ),
        }
