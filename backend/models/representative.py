from sqlalchemy import String, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from .base import Base
import uuid
from datetime import datetime

class Person(Base):
    __tablename__ = 'rep_person'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name: Mapped[str] = mapped_column(String(255))
    raw_source_name: Mapped[str] = mapped_column(String(255), nullable=True)

class Party(Base):
    __tablename__ = 'rep_party'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255))

class Position(Base):
    __tablename__ = 'rep_position'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255))
    level: Mapped[str] = mapped_column(String(100))

class Term(Base):
    __tablename__ = 'rep_term'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    person_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('rep_person.id'))
    position_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('rep_position.id'))
    party_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('rep_party.id'), nullable=True)
    jurisdiction_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('geo_entity.id'))
    valid_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    valid_until: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        CheckConstraint('valid_until >= valid_from', name='check_valid_dates_term'),
    )
