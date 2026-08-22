from sqlalchemy import String, ForeignKey, DateTime, Integer, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from .base import Base
import uuid
from datetime import datetime

class Source(Base):
    """Registered official data source."""
    __tablename__ = 'src_source'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    public_id: Mapped[str] = mapped_column(String(100), nullable=True, unique=True)
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    official_name: Mapped[str] = mapped_column(String(512), nullable=True)
    authority_name: Mapped[str] = mapped_column(String(512), nullable=True)
    authority_type: Mapped[str] = mapped_column(String(100), nullable=True)
    authority_level: Mapped[str] = mapped_column(String(100), nullable=True)
    government_level: Mapped[str] = mapped_column(String(100), nullable=True)
    country: Mapped[str] = mapped_column(String(100), nullable=True, default="India")
    state: Mapped[str] = mapped_column(String(100), nullable=True)
    district: Mapped[str] = mapped_column(String(100), nullable=True)
    department: Mapped[str] = mapped_column(String(256), nullable=True)
    category: Mapped[str] = mapped_column(String(100), nullable=True)
    subcategory: Mapped[str] = mapped_column(String(100), nullable=True)
    jurisdiction: Mapped[str] = mapped_column(String(200), nullable=True)
    official_domain: Mapped[str] = mapped_column(String(2048), nullable=True)
    canonical_url: Mapped[str] = mapped_column(String(2048), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    source_type: Mapped[str] = mapped_column(String(100), nullable=True)
    access_method: Mapped[str] = mapped_column(String(100), nullable=True)
    license: Mapped[str] = mapped_column(String(200), nullable=True)
    attribution: Mapped[str] = mapped_column(Text, nullable=True)
    terms_url: Mapped[str] = mapped_column(String(2048), nullable=True)
    robots_policy: Mapped[str] = mapped_column(String(200), nullable=True)
    contact_url: Mapped[str] = mapped_column(String(2048), nullable=True)
    api_available: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    authentication_required: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    rate_limit: Mapped[str] = mapped_column(String(100), nullable=True)
    refresh_policy: Mapped[str] = mapped_column(String(100), nullable=True)
    priority: Mapped[int] = mapped_column(Integer, default=3, nullable=True)
    trust_level: Mapped[str] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="ACTIVE")
    access_policy: Mapped[str] = mapped_column(String(200), nullable=True)
    discovered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=True)
    verified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    last_checked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    last_success_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    last_failure_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    next_scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)


class SourceEndpoint(Base):
    __tablename__ = 'src_endpoint'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_source.id'), nullable=False)
    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    canonical_url: Mapped[str] = mapped_column(String(2048), nullable=True)
    method: Mapped[str] = mapped_column(String(10), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="ACTIVE")
    redirect_url: Mapped[str] = mapped_column(String(2048), nullable=True)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    endpoint_schema: Mapped[dict] = mapped_column(JSONB, nullable=True)
    endpoint_type: Mapped[str] = mapped_column(String(100), nullable=True)
    expected_format: Mapped[str] = mapped_column(String(100), nullable=True)
    discovery_method: Mapped[str] = mapped_column(String(100), nullable=True)
    refresh_frequency: Mapped[str] = mapped_column(String(100), nullable=True)
    priority: Mapped[int] = mapped_column(Integer, default=3, nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=True)
    error_count: Mapped[int] = mapped_column(Integer, default=0, nullable=True)
    retry_count: Mapped[int] = mapped_column(Integer, default=0, nullable=True)
    last_checked: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    last_success: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    last_failure: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    next_scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    checksum: Mapped[str] = mapped_column(String(256), nullable=True)
    source = relationship("Source")


class Dataset(Base):
    __tablename__ = 'src_dataset'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_source.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(512), nullable=False)


class IngestionRun(Base):
    __tablename__ = 'src_ingestion_run'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dataset_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_dataset.id'), nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)


class FetchEvent(Base):
    __tablename__ = 'src_fetch_event'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_ingestion_run.id'), nullable=False)
    endpoint_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_endpoint.id'), nullable=True)
    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    status_code: Mapped[int] = mapped_column(Integer(), nullable=True)
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    content_length: Mapped[int] = mapped_column(Integer(), nullable=True)
    etag: Mapped[str] = mapped_column(String(256), nullable=True)
    last_modified: Mapped[str] = mapped_column(String(256), nullable=True)
    redirect_chain: Mapped[dict] = mapped_column(JSONB, nullable=True)
    error_message: Mapped[str] = mapped_column(Text, nullable=True)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=True) # Hash seen during this fetch


class Document(Base):
    __tablename__ = 'src_document'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_source.id'), nullable=True)
    document_type: Mapped[str] = mapped_column(String(100), nullable=True)
    title: Mapped[str] = mapped_column(String(1024), nullable=True)
    publication_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    canonical_url: Mapped[str] = mapped_column(String(2048), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="CURRENT")
    relationship: Mapped[str] = mapped_column(String(50), nullable=True) # e.g. CORRIGENDUM
    related_document_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_document.id'), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


class ContentVersion(Base):
    __tablename__ = 'src_content_version'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_document.id'), nullable=False)
    version_number: Mapped[int] = mapped_column(Integer(), nullable=False)
    sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    byte_size: Mapped[int] = mapped_column(Integer(), nullable=True)
    mime_type: Mapped[str] = mapped_column(String(256), nullable=True)
    page_count: Mapped[int] = mapped_column(Integer(), nullable=True)
    storage_path: Mapped[str] = mapped_column(String(1024), nullable=True)
    retrieved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
