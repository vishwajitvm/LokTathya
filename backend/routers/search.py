from fastapi import APIRouter, Request, Query, Depends
from sqlalchemy.orm import Session
from tracenest import logger
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
    logger.info("GET /api/v1/search – Hybrid search invoked", query=query, jurisdiction=jurisdiction, limit=limit, offset=offset)
    logger.debug("Database session acquired for search query", session_id=str(id(db)))
    logger.debug("Search parameters parsed", query_text=query, jurisdiction_filter=jurisdiction, pagination_limit=limit, pagination_offset=offset)

    # Search is currently not implemented against DB; return empty to avoid fake data
    logger.warning("Search engine NOT YET IMPLEMENTED – returning empty result set", query=query)
    result = PaginatedResponse(
        data=[],
        meta=PaginationMeta(limit=limit, offset=offset, has_more=False)
    )
    logger.info("Search response assembled", result_count=0, has_more=False)
    return result
