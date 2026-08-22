from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime
from uuid import UUID

class SourceBase(BaseModel):
    name: str
    official_name: Optional[str] = None
    authority_name: Optional[str] = None
    authority_type: Optional[str] = None
    authority_level: Optional[str] = None
    government_level: Optional[str] = None
    country: Optional[str] = "India"
    state: Optional[str] = None
    district: Optional[str] = None
    department: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    official_domain: Optional[str] = None
    description: Optional[str] = None
    source_type: Optional[str] = None
    license: Optional[str] = None
    robots_policy: Optional[str] = None
    priority: Optional[int] = 3
    trust_level: Optional[str] = None
    status: Optional[str] = "ACTIVE"

class SourceCreate(SourceBase):
    pass

class SourceResponse(SourceBase):
    id: UUID
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class EndpointBase(BaseModel):
    url: str
    method: str = "GET"
    status: Optional[str] = "ACTIVE"

class EndpointCreate(EndpointBase):
    source_id: UUID

class EndpointResponse(EndpointBase):
    id: UUID
    source_id: UUID

    class Config:
        from_attributes = True
