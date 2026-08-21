from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uuid

router = APIRouter(prefix="/api/v1/chat", tags=["Civic AI Chat"])

class ChatRequest(BaseModel):
    question: str
    session_context: Optional[Dict[str, Any]] = None
    geography_context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    request_id: str
    answer_blocks: List[Dict[str, Any]]
    citations: List[Dict[str, Any]]

@router.post("/", response_model=ChatResponse)
def handle_chat(req: ChatRequest, request: Request):
    return ChatResponse(
        request_id=getattr(request.state, "request_id", str(uuid.uuid4())),
        answer_blocks=[{"type": "TEXT", "content": "Civic AI backend is currently unconfigured."}],
        citations=[]
    )
