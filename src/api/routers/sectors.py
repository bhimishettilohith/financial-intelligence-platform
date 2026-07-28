"""
Sector API Router
"""

from fastapi import APIRouter, HTTPException, Request

from src.api.services.sector_service import SectorService

router = APIRouter(
    prefix="/sectors",
    tags=["Sectors"],
)


@router.get("")
def get_sectors(request: Request):

    conn = request.app.state.get_db_connection()

    service = SectorService(conn)

    return service.get_all_sectors()


@router.get("/{sector}/companies")
def get_sector_companies(
    sector: str,
    request: Request,
):

    conn = request.app.state.get_db_connection()

    service = SectorService(conn)

    companies = service.get_sector_companies(sector)

    if companies is None:
        raise HTTPException(
            status_code=404,
            detail="Sector not found",
        )

    return companies
