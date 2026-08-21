from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from .base import Base
import uuid

class Claim(Base):
    __tablename__ = 'prov_claim'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_level: Mapped[str] = mapped_column(String(50)) # DATASET, DOCUMENT, RECORD, CLAIM
    description: Mapped[str] = mapped_column(String(1024))

class Evidence(Base):
    __tablename__ = 'prov_evidence'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('prov_claim.id'))
    source_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_source.id'))
    content_version_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_content_version.id'), nullable=True)
