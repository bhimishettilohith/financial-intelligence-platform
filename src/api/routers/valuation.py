"""
Valuation API Router
"""

from fastapi import APIRouter, Request

from src.api.services.valuation_service import ValuationService

router = APIRouter(
    prefix="/market-cap",
    tags=["Market Cap"],
)


@router.get("/{ticker}")
def get_market_cap(
    ticker: str,
    request: Request,
):

    service = ValuationService(request.app.state.get_db_connection())

    return service.get_market_cap_history(ticker)
