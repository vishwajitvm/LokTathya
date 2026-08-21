from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime
from uuid import UUID


class SourceBase(BaseModel):
    name: str
    category: Optional[str] = None
    official_url: Optional[str] = None


class SourceCreate(SourceBase):
    pass


class SourceResponse(SourceBase):
    id: UUID
    last_fetched: Optional[datetime] = None

    class Config:
        from_attributes = True


class EndpointBase(BaseModel):
    url: str
    method: str = "GET"


class EndpointCreate(EndpointBase):
    source_id: UUID


class EndpointResponse(EndpointBase):
    id: UUID
    source_id: UUID

    class Config:
        from_attributes = True
