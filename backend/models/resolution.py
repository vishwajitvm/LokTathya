from sqlalchemy import Column, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, JSONB
from .base import Base
import uuid
from datetime import datetime

class EntityResolution(Base):
    __tablename__ = 'sys_entity_resolution'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_source.id'))
    raw_value: Mapped[str] = mapped_column(String(1024))
    target_table: Mapped[str] = mapped_column(String(100))
    candidate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=True)
    matching_method: Mapped[str] = mapped_column(String(100))
    confidence: Mapped[float] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String(50)) # UNRESOLVED, CANDIDATE, AUTO_ACCEPTED, HUMAN_REVIEW, CONFIRMED, REJECTED
    reviewer: Mapped[str] = mapped_column(String(255), nullable=True)
    resolved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
