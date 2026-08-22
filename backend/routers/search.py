from fastapi import APIRouter, Request, Query, Depends
from sqlalchemy.orm import Session
from tracenest import logger
from schemas.base_schema import PaginatedResponse, PaginationMeta
from core.database import get_db
from models.provenance import CanonicalFact

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
    
    query_str = f"%{query}%"
    facts = db.query(CanonicalFact).filter(
        (CanonicalFact.attribute_name.ilike(query_str)) |
        (CanonicalFact.entity_id.ilike(query_str))
    ).offset(offset).limit(limit).all()
    
    data = [
        {
            "id": str(f.id),
            "title": f"Canonical Fact: {f.attribute_name}",
            "snippet": f"Value: {f.value.get('value') if isinstance(f.value, dict) else f.value}",
            "url": f"/api/v1/canonical-facts/{f.id}"
        }
        for f in facts
    ]
    
    result = PaginatedResponse(
        data=data,
        meta=PaginationMeta(limit=limit, offset=offset, has_more=len(facts) == limit)
    )
    return result
