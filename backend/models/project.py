from sqlalchemy import String, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from .base import Base
import uuid

class Project(Base):
    __tablename__ = 'proj_project'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(1024))
    raw_name: Mapped[str] = mapped_column(String(1024))

class Work(Base):
    __tablename__ = 'proj_work'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('proj_project.id'))
    name: Mapped[str] = mapped_column(String(1024))

class Contractor(Base):
    __tablename__ = 'proj_contractor'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255))

class Tender(Base):
    __tablename__ = 'proj_tender'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    work_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('proj_work.id'))
    tender_reference: Mapped[str] = mapped_column(String(255))

class Contract(Base):
    __tablename__ = 'proj_contract'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tender_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('proj_tender.id'), nullable=True)
    contractor_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('proj_contractor.id'), nullable=True)
    amount: Mapped[float] = mapped_column(Numeric(15, 2))
