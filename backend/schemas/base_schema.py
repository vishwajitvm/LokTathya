from pydantic import BaseModel, Field
from typing import List, Optional, Any
from uuid import UUID
from datetime import datetime

class ApiError(BaseModel):
    code: str
    message: str
    details: Optional[str] = None
    request_id: str

class PaginationMeta(BaseModel):
    limit: int
    offset: int
    total: Optional[int] = None
    has_more: bool

class PaginatedResponse(BaseModel):
    data: List[Any]
    meta: PaginationMeta

class CitationDTO(BaseModel):
    source_name: str
    authority: str
    official_url: str
    document_title: Optional[str] = None
    publication_date: Optional[datetime] = None
    content_version_id: Optional[UUID] = None
    page: Optional[int] = None
    section: Optional[str] = None
    retrieved_at: datetime
