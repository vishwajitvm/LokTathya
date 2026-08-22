from sqlalchemy import String, ForeignKey, DateTime, Integer, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from .base import Base
import uuid
from datetime import datetime


class ExtractedTextVersion(Base):
    __tablename__ = 'src_extracted_text_version'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_version_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_content_version.id'), nullable=False)
    parser_version: Mapped[str] = mapped_column(String(50), nullable=False)
    extraction_method: Mapped[str] = mapped_column(String(100), nullable=True)
    output_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    extracted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


class OCRVersion(Base):
    __tablename__ = 'src_ocr_version'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_version_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_content_version.id'), nullable=False)
    ocr_engine: Mapped[str] = mapped_column(String(100), nullable=False)
    ocr_engine_version: Mapped[str] = mapped_column(String(50), nullable=False)
    ocr_configuration: Mapped[dict] = mapped_column(JSONB, nullable=True)
    language: Mapped[str] = mapped_column(String(50), nullable=True)
    output_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


class ChunkVersion(Base):
    __tablename__ = 'src_chunk_version'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_version_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_content_version.id'), nullable=False)
    chunker_version: Mapped[str] = mapped_column(String(50), nullable=False)
    chunking_policy_version: Mapped[str] = mapped_column(String(50), nullable=True)
    chunk_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    position: Mapped[int] = mapped_column(Integer(), nullable=True)
    page: Mapped[int] = mapped_column(Integer(), nullable=True)
    heading: Mapped[str] = mapped_column(String(256), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


class EmbeddingVersion(Base):
    __tablename__ = 'src_embedding_version'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chunk_version_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_chunk_version.id'), nullable=True)
    content_version_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_content_version.id'), nullable=True)
    embedding_model: Mapped[str] = mapped_column(String(100), nullable=False)
    embedding_model_version: Mapped[str] = mapped_column(String(50), nullable=False)
    embedding_dimension: Mapped[int] = mapped_column(Integer(), nullable=False)
    embedding_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
