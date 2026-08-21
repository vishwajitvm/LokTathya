from fastapi import APIRouter, Request, Query, Depends
from sqlalchemy.orm import Session
from schemas.base_schema import PaginatedResponse, PaginationMeta
from core.database import get_db

router = APIRouter(prefix="/api/v1/search", tags=["Search"])

@router.get("/", response_model=PaginatedResponse)
def hybrid_search(
    request: Request,
    query: str,
    jurisdiction: str = Query(None),
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    # Search is currently not implemented against DB; return empty to avoid fake data
    return PaginatedResponse(
        data=[],
        meta=PaginationMeta(limit=limit, offset=offset, has_more=False)
    )
