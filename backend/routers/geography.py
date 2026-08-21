from fastapi import APIRouter
from schemas.base_schema import PaginatedResponse, PaginationMeta
import uuid

router = APIRouter(prefix="/api/v1/geographies", tags=["Geography"])

@router.get("/", response_model=PaginatedResponse)
def list_geographies(limit: int = 50, offset: int = 0):
    return PaginatedResponse(data=[], meta=PaginationMeta(limit=limit, offset=offset, has_more=False))
