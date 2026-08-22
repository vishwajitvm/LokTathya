from fastapi import APIRouter
from tracenest import logger
from schemas.base_schema import PaginatedResponse, PaginationMeta

router = APIRouter(prefix="/api/v1/geographies", tags=["Geography"])

@router.get("/", response_model=PaginatedResponse)
def list_geographies(limit: int = 50, offset: int = 0):
    logger.info("GET /api/v1/geographies – Listing geographies", limit=limit, offset=offset)
    logger.debug("Geography listing parameters", pagination_limit=limit, pagination_offset=offset)

    result = PaginatedResponse(data=[], meta=PaginationMeta(limit=limit, offset=offset, has_more=False))
    logger.info("Geography listing completed", result_count=0, has_more=False)
    return result
