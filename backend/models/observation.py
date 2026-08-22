from sqlalchemy import Column, String, DateTime, ForeignKey, Text, JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from models.base import Base
import uuid
from datetime import datetime

class Observation(Base):
    """
    Priority 1: Raw Observation captured from parsed and normalized document content.
    Prevents direct overwriting of canonical entities.
    """
    __tablename__ = 'src_observation'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(ForeignKey('src_source.id', ondelete='CASCADE'), nullable=False, index=True)
    document_id = Column(ForeignKey('src_document.id', ondelete='CASCADE'), nullable=True, index=True)
    content_version_id = Column(ForeignKey('src_content_version.id', ondelete='CASCADE'), nullable=True, index=True)
    
    web_page_id = Column(ForeignKey('src_web_page.id', ondelete='CASCADE'), nullable=True, index=True)
    web_page_version_id = Column(ForeignKey('src_web_page_version.id', ondelete='CASCADE'), nullable=True, index=True)

    entity_type = Column(String(100), nullable=False) # e.g. representative, election_result, budget_allocation
    field_name = Column(String(255), nullable=False)
    
    raw_value = Column(Text, nullable=False)
    normalized_value = Column(JSONB, nullable=True) # Normalized structured value
    
    extraction_location = Column(String(512), nullable=True) # e.g. "page 2, table 0, row 3"
    observed_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    status = Column(String(50), default="VALIDATED") # VALIDATED, CONFLICTING, QUARANTINED, SUPERSEDED
