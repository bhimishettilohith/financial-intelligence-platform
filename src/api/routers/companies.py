"""
Sprint 6 - Day 39

Company API endpoints.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import FileResponse

from src.api.services.company_service import CompanyService

router = APIRouter()


def get_service(request: Request) -> CompanyService:
    """
    Create a CompanyService instance using the shared SQLite connection.
    """
    conn = request.app.state.get_db_connection()
    return CompanyService(conn)


# ---------------------------------------------------------------------
# GET /companies
# ---------------------------------------------------------------------


@router.get("/companies")
def get_companies(
    request: Request,
    sector: str | None = Query(default=None),
    market_cap_category: str | None = Query(default=None),
    search: str | None = Query(default=None),
):
    """
    Return list of companies.
    """

    service = get_service(request)

    companies = service.get_company_list(
        sector=sector,
        market_cap_category=market_cap_category,
        search=search,
    )

    return {
        "count": len(companies),
        "data": companies,
    }


# ---------------------------------------------------------------------
# GET /companies/{ticker}
# ---------------------------------------------------------------------


@router.get("/companies/{ticker}")
def get_company_profile(
    ticker: str,
    request: Request,
):
    """
    Return company profile.
    """

    service = get_service(request)

    company = service.get_company_profile(ticker)

    if company is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found",
        )

    return company


# ---------------------------------------------------------------------
# GET /companies/{ticker}/pl
# ---------------------------------------------------------------------


@router.get("/companies/{ticker}/pl")
def get_profit_loss(
    ticker: str,
    request: Request,
    from_year: str | None = Query(default=None),
    to_year: str | None = Query(default=None),
):
    """
    Return P&L history.
    """

    service = get_service(request)

    data = service.get_profit_loss(
        ticker=ticker,
        from_year=from_year,
        to_year=to_year,
    )

    return {
        "ticker": ticker,
        "count": len(data),
        "data": data,
    }


# ---------------------------------------------------------------------
# GET /companies/{ticker}/bs
# ---------------------------------------------------------------------


@router.get("/companies/{ticker}/bs")
def get_balance_sheet(
    ticker: str,
    request: Request,
    from_year: str | None = Query(default=None),
    to_year: str | None = Query(default=None),
):
    """
    Return balance sheet history.
    """

    service = get_service(request)

    data = service.get_balance_sheet(
        ticker=ticker,
        from_year=from_year,
        to_year=to_year,
    )

    return {
        "ticker": ticker,
        "count": len(data),
        "data": data,
    }


# ---------------------------------------------------------------------
# GET /companies/{ticker}/cashflow
# ---------------------------------------------------------------------


@router.get("/companies/{ticker}/cashflow")
def get_cashflow(
    ticker: str,
    request: Request,
    from_year: str | None = Query(default=None),
    to_year: str | None = Query(default=None),
):
    """
    Return cashflow history.
    """

    service = get_service(request)

    data = service.get_cashflow(
        ticker=ticker,
        from_year=from_year,
        to_year=to_year,
    )

    return {
        "ticker": ticker,
        "count": len(data),
        "data": data,
    }


# ---------------------------------------------------------------------
# GET /companies/{ticker}/ratios
# ---------------------------------------------------------------------


@router.get("/companies/{ticker}/ratios")
def get_ratios(
    ticker: str,
    request: Request,
    year: str | None = Query(default=None),
):
    """
    Return financial ratios.
    """

    service = get_service(request)

    data = service.get_ratios(
        ticker=ticker,
        year=year,
    )

    return {
        "ticker": ticker,
        "count": len(data),
        "data": data,
    }


# ---------------------------------------------------------------------
# GET /companies/{ticker}/tearsheet
# ---------------------------------------------------------------------


@router.get("/companies/{ticker}/tearsheet")
def get_tearsheet(
    ticker: str,
    request: Request,
):
    """
    Download pre-generated company tearsheet.
    """

    service = get_service(request)

    pdf_path = service.get_tearsheet_path(ticker)

    if pdf_path is None:
        raise HTTPException(
            status_code=404,
            detail="Tearsheet not found",
        )

    return FileResponse(
        path=str(pdf_path),
        media_type="application/pdf",
        filename=pdf_path.name,
    )
