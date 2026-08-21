from sqlalchemy import String, ForeignKey, Integer, Column
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from .base import Base
import uuid

class EmbeddingModel(Base):
    __tablename__ = 'ai_embedding_model'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100))
    version: Mapped[str] = mapped_column(String(50))
    dimensions: Mapped[int] = mapped_column(Integer)

class Chunk(Base):
    __tablename__ = 'ai_chunk'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_document.id'))
    content_version_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('src_content_version.id'))
    chunk_index: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(String)
    
class Embedding(Base):
    __tablename__ = 'ai_embedding'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chunk_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('ai_chunk.id'))
    model_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('ai_embedding_model.id'))
    vector = Column(Vector(1536))
