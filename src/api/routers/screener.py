"""
Screener API Router
"""

from fastapi import APIRouter, HTTPException, Query, Request

from src.api.services.screener_service import ScreenerService

router = APIRouter(prefix="/screener", tags=["Screener"])


@router.get("")
def get_screener(
    request: Request,
    min_roe: float | None = Query(None, ge=0),
    max_de: float | None = Query(None, ge=0),
    min_fcf: float | None = Query(None),
    sector: str | None = Query(None),
    min_rev_cagr_5yr: float | None = Query(None),
    min_pat_cagr_5yr: float | None = Query(None),
    max_pe: float | None = Query(None),
):
    """
    Screen companies using financial filters.
    """

    # P/E data is unavailable in the current database.
    if max_pe is not None:
        raise HTTPException(
            status_code=400,
            detail=(
                "Filtering by max_pe is not supported because "
                "P/E data is unavailable in the current dataset."
            ),
        )

    conn = request.app.state.get_db_connection()

    service = ScreenerService(conn)

    return service.screen_companies(
        min_roe=min_roe,
        max_de=max_de,
        min_fcf=min_fcf,
        sector=sector,
        min_rev_cagr_5yr=min_rev_cagr_5yr,
        min_pat_cagr_5yr=min_pat_cagr_5yr,
    )
