"""
Peer API Router
"""

from fastapi import APIRouter, HTTPException, Request

from src.api.services.peer_service import PeerService

router = APIRouter(
    prefix="/peers",
    tags=["Peers"],
)


@router.get("/{group_name}")
def get_peer_group(
    group_name: str,
    request: Request,
):

    service = PeerService(request.app.state.get_db_connection())

    data = service.get_peer_group(group_name)

    if data is None:
        raise HTTPException(
            status_code=404,
            detail="Peer group not found",
        )

    return data


@router.get("/company/{ticker}/compare")
def compare_company(
    ticker: str,
    request: Request,
):

    service = PeerService(request.app.state.get_db_connection())

    data = service.compare_company_with_peers(ticker)

    if data is None:
        raise HTTPException(
            status_code=404,
            detail="Company or peer group not found",
        )

    return data
