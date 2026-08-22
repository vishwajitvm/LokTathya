from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from tracenest import logger
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
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    logger.info("POST /api/v1/chat – Civic AI chat request received", request_id=request_id)
    logger.debug("Chat question received", question=req.question[:200], has_session_context=bool(req.session_context), has_geography_context=bool(req.geography_context))

    logger.debug("Building grounded prompt context", request_id=request_id)
    logger.warning("Civic AI RAG pipeline NOT YET CONFIGURED – returning placeholder response", request_id=request_id)

    response = ChatResponse(
        request_id=request_id,
        answer_blocks=[{"type": "TEXT", "content": "Civic AI backend is currently unconfigured."}],
        citations=[]
    )
    logger.info("Chat response assembled", request_id=request_id, answer_block_count=len(response.answer_blocks), citation_count=len(response.citations))
    return response
