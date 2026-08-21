from sqlalchemy import String, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from .base import Base
import uuid
from datetime import datetime

class FinancialYear(Base):
    __tablename__ = 'fin_year'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    label: Mapped[str] = mapped_column(String(20), unique=True)
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))

class Budget(Base):
    __tablename__ = 'fin_budget'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    year_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('fin_year.id'))
    amount: Mapped[float] = mapped_column(Numeric(15, 2))
    currency: Mapped[str] = mapped_column(String(3), default='INR')
    original_source_value: Mapped[str] = mapped_column(String(255))

class BudgetAllocation(Base):
    __tablename__ = 'fin_allocation'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('proj_project.id'))
    budget_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('fin_budget.id'))
    amount: Mapped[float] = mapped_column(Numeric(15, 2))
    currency: Mapped[str] = mapped_column(String(3), default='INR')

class FundRelease(Base):
    __tablename__ = 'fin_release'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    allocation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('fin_allocation.id'))
    amount: Mapped[float] = mapped_column(Numeric(15, 2))
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True))

class Expenditure(Base):
    __tablename__ = 'fin_expenditure'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    work_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('proj_work.id'))
    amount: Mapped[float] = mapped_column(Numeric(15, 2))
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
