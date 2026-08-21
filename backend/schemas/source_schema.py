from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class SourceBase(BaseModel):
    public_id: str
    authority: str
    status: str

class SourceCreate(SourceBase):
    pass

class SourceResponse(SourceBase):
    id: UUID
    class Config:
        from_attributes = True

class EndpointBase(BaseModel):
    official_url: HttpUrl

class EndpointCreate(EndpointBase):
    source_id: UUID

class EndpointResponse(EndpointBase):
    id: UUID
    source_id: UUID
    class Config:
        from_attributes = True
