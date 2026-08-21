from sqlalchemy import Column, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, JSONB
from .base import Base
import uuid
from datetime import datetime

class Claim(Base):
    __tablename__ = 'prov_claim'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_type: Mapped[str] = mapped_column(String(50)) # OFFICIAL, DERIVED
    description: Mapped[str] = mapped_column(String(1024))

class Evidence(Base):
    __tablename__ = 'prov_evidence'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('prov_claim.id'))
    source_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_source.id'))
    content_version_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_content_version.id'), nullable=True)
    location_in_doc: Mapped[str] = mapped_column(String(255), nullable=True)
