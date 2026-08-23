import uuid
from datetime import datetime
from typing import Optional, Any
from sqlalchemy import String, DateTime, ForeignKey, Boolean, JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, JSONB
from models.base import Base

class Dataset(Base):
    """
    Core dataset identity representing a logical collection of records over time.
    """
    __tablename__ = 'src_dataset'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_source.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE")

class DatasetVersion(Base):
    """
    Immutable snapshots of a Dataset at a particular point in time.
    """
    __tablename__ = 'src_dataset_version'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dataset_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_dataset.id'), nullable=False)
    source_endpoint_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_endpoint.id'), nullable=True)
    content_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    valid_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    valid_until: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    change_classification: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

class DatasetSchema(Base):
    """
    Inferred structure (columns, types, constraints) for a specific dataset version.
    """
    __tablename__ = 'src_dataset_schema'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dataset_version_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_dataset_version.id'), nullable=False)
    inferred_schema: Mapped[dict] = mapped_column(JSONB, nullable=False)  # stores list of inferred columns/types
    inferred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class DatasetField(Base):
    """
    Semantic mapping for a specific column/field inferred in the schema.
    """
    __tablename__ = 'src_dataset_field'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dataset_schema_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_dataset_schema.id'), nullable=False)
    original_name: Mapped[str] = mapped_column(String(255), nullable=False)
    semantic_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True) # e.g. DISTRICT, PERSON, CURRENCY
    confidence: Mapped[Optional[float]] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="MAPPED")

class DatasetQualityProfile(Base):
    """
    Statistics and quality metrics for a dataset version.
    """
    __tablename__ = 'src_dataset_quality_profile'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dataset_version_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_dataset_version.id'), nullable=False)
    row_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    column_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    null_ratio: Mapped[float] = mapped_column(nullable=True)
    duplicate_row_ratio: Mapped[float] = mapped_column(nullable=True)
    profiled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class DatasetRelationship(Base):
    """
    Relationships between datasets (e.g., supersedes, derives_from).
    """
    __tablename__ = 'src_dataset_relationship'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_dataset_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_dataset.id'), nullable=False)
    target_dataset_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_dataset.id'), nullable=False)
    relationship_type: Mapped[str] = mapped_column(String(100), nullable=False) # e.g. SUPERSEDES, DERIVES_FROM
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
