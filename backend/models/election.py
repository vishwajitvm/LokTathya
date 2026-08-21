from sqlalchemy import String, ForeignKey, DateTime, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from .base import Base
import uuid
from datetime import datetime

class Election(Base):
    __tablename__ = 'elec_election'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    public_id: Mapped[str] = mapped_column(String(50), unique=True)
    type: Mapped[str] = mapped_column(String(50))
    year: Mapped[int] = mapped_column(Integer)

class ElectionResult(Base):
    __tablename__ = 'elec_result'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    election_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('elec_election.id'))
    person_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('rep_person.id'))
    party_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('rep_party.id'), nullable=True)
    votes: Mapped[int] = mapped_column(Integer, nullable=True)
    vote_percentage: Mapped[float] = mapped_column(Float, nullable=True)
    rank: Mapped[int] = mapped_column(Integer, nullable=True)
