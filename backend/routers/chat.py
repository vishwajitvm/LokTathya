from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from ai.planner import QueryPlanner
from ai.validator import CitationValidator
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
    planner = QueryPlanner()
    validator = CitationValidator()
    
    # 1. Plan & Execute Tools
    plan = planner.plan(req.question)
    evidence = planner.execute(plan, req.question)
    
    # 2. LLM Generation (Mocked)
    raw_llm_response = "Based on the evidence, the utilization rate is 50%."
    
    # 3. Validation
    validation_result = validator.validate(raw_llm_response, evidence)
    
    return ChatResponse(
        request_id=getattr(request.state, "request_id", str(uuid.uuid4())),
        answer_blocks=[{"type": "TEXT", "content": validation_result["validated_text"]}],
        citations=validation_result["citations"]
    )
