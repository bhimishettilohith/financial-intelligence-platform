"""
Documents API Router
"""

from fastapi import APIRouter, HTTPException, Request

from src.api.services.document_service import DocumentService

router = APIRouter(
    prefix="/companies",
    tags=["Documents"],
)


@router.get("/{ticker}/documents")
def get_documents(
    ticker: str,
    request: Request,
):

    service = DocumentService(request.app.state.get_db_connection())

    docs = service.get_company_documents(ticker)

    if docs is None:
        raise HTTPException(
            status_code=404,
            detail="Company documents not found",
        )

    return docs
