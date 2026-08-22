from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Boolean, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, JSONB
from .base import Base
import uuid
from datetime import datetime

class Claim(Base):
    __tablename__ = 'prov_claim'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_level: Mapped[str] = mapped_column(String(50)) # DATASET, DOCUMENT, RECORD, CLAIM
    description: Mapped[str] = mapped_column(String(1024))
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    valid_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    valid_until: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="CURRENT") # CURRENT, SUPERSEDED
    canonical_fact_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('prov_canonical_fact.id'), nullable=True)


class CanonicalFact(Base):
    __tablename__ = 'prov_canonical_fact'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_id: Mapped[str] = mapped_column(String(256), nullable=False) # abstract identifier
    attribute_name: Mapped[str] = mapped_column(String(256), nullable=False)
    value: Mapped[dict] = mapped_column(JSONB, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="CURRENT")
    conflict_status: Mapped[str] = mapped_column(String(50), default="CONSISTENT") # CONSISTENT, MINOR_VARIANCE, CONFLICTING, UNRESOLVED
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    claims = relationship("Claim", backref="canonical_fact")


class Evidence(Base):
    __tablename__ = 'prov_evidence'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('prov_claim.id'))
    source_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_source.id'))
    endpoint_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_endpoint.id'), nullable=True)
    document_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_document.id'), nullable=True)
    content_version_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_content_version.id'), nullable=True)
    page_number: Mapped[int] = mapped_column(Integer(), nullable=True)
    extracted_text_version_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_extracted_text_version.id'), nullable=True)
    record_id: Mapped[str] = mapped_column(String(256), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
