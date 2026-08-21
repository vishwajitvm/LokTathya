from sqlalchemy import String, ForeignKey, DateTime, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from .base import Base
import uuid
from datetime import datetime

class Project(Base):
    __tablename__ = 'proj_project'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    public_id: Mapped[str] = mapped_column(String(50), unique=True)
    name: Mapped[str] = mapped_column(String(1024))
    status: Mapped[str] = mapped_column(String(50))

class FinancialYear(Base):
    __tablename__ = 'fin_year'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    label: Mapped[str] = mapped_column(String(20), unique=True)
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))

class BudgetAllocation(Base):
    __tablename__ = 'fin_allocation'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('proj_project.id'), nullable=True)
    financial_year_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('fin_year.id'))
    amount: Mapped[float] = mapped_column(Numeric(15, 2))
    currency: Mapped[str] = mapped_column(String(3), default='INR')
    original_source_value: Mapped[str] = mapped_column(String(255))
