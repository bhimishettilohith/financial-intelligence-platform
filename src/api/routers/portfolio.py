"""
Portfolio API Router
"""

from fastapi import APIRouter, Request

from src.api.services.portfolio_service import PortfolioService

router = APIRouter(
    prefix="/portfolio",
    tags=["Portfolio"],
)


@router.get("/stats")
def get_portfolio_stats(request: Request):

    service = PortfolioService(request.app.state.get_db_connection())

    return service.get_percentile_stats()
