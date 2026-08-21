from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

class FetchResult(BaseModel):
    source_id: uuid.UUID
    endpoint_id: uuid.UUID
    fetch_event_id: uuid.UUID
    retrieved_at: datetime
    http_status: Optional[int] = None
    content_type: Optional[str] = None
    content_length: Optional[int] = None
    content_hash: Optional[str] = None
    etag: Optional[str] = None
    last_modified: Optional[str] = None
    raw_object_location: Optional[str] = None
    fetch_status: str

class BaseConnector:
    def discover(self):
        raise NotImplementedError
    
    def fetch(self, endpoint_url: str) -> FetchResult:
        raise NotImplementedError

    def parse(self, fetch_result: FetchResult) -> list[Dict[str, Any]]:
        raise NotImplementedError

    def validate(self, parsed_data: list[Dict[str, Any]]) -> list[Dict[str, Any]]:
        raise NotImplementedError
