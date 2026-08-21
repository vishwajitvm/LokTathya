from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, JSONB
from .base import Base
import uuid
from datetime import datetime

class Source(Base):
    __tablename__ = 'src_source'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    public_id: Mapped[str] = mapped_column(String(50), unique=True)
    authority: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50))

class SourceEndpoint(Base):
    __tablename__ = 'src_endpoint'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_source.id'))
    official_url: Mapped[str] = mapped_column(String(1024))

class Dataset(Base):
    __tablename__ = 'src_dataset'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_source.id'))
    name: Mapped[str] = mapped_column(String(255))

class IngestionRun(Base):
    __tablename__ = 'src_ingestion_run'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    status: Mapped[str] = mapped_column(String(50))

class FetchEvent(Base):
    __tablename__ = 'src_fetch_event'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    endpoint_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_endpoint.id'))
    run_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_ingestion_run.id'))
    fetch_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    status_code: Mapped[int] = mapped_column(Integer, nullable=True)

class Document(Base):
    __tablename__ = 'src_document'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dataset_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_dataset.id'))
    title: Mapped[str] = mapped_column(String(1024))
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    retrieved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class ContentVersion(Base):
    __tablename__ = 'src_content_version'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_document.id'))
    fetch_event_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_fetch_event.id'))
    content_hash: Mapped[str] = mapped_column(String(64), index=True)
    storage_path: Mapped[str] = mapped_column(String(1024))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
