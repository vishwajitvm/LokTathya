from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean, Text
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
    official_url: Mapped[str] = mapped_column(String(1024))
    domain: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(50)) # DISCOVERED, ACTIVE, RETIRED

class Dataset(Base):
    __tablename__ = 'src_dataset'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_source.id'))
    name: Mapped[str] = mapped_column(String(255))

class Document(Base):
    __tablename__ = 'src_document'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    public_id: Mapped[str] = mapped_column(String(50), unique=True)
    dataset_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_dataset.id'))
    title: Mapped[str] = mapped_column(String(1024))
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    retrieved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class ContentVersion(Base):
    __tablename__ = 'src_content_version'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_document.id'))
    content_hash: Mapped[str] = mapped_column(String(64), index=True)
    storage_path: Mapped[str] = mapped_column(String(1024))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
