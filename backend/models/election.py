from sqlalchemy import String, ForeignKey, Integer, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from .base import Base
import uuid
from datetime import datetime

class Election(Base):
    __tablename__ = 'elec_election'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type: Mapped[str] = mapped_column(String(50))
    year: Mapped[int] = mapped_column(Integer)

class ElectionEvent(Base):
    __tablename__ = 'elec_event'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    election_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('elec_election.id'))
    phase: Mapped[int] = mapped_column(Integer, nullable=True)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

class Candidate(Base):
    __tablename__ = 'elec_candidate'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    person_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('rep_person.id'), nullable=True)
    party_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('rep_party.id'), nullable=True)
    raw_name: Mapped[str] = mapped_column(String(255))

class ElectionResult(Base):
    __tablename__ = 'elec_result'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('elec_event.id'))
    constituency_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('geo_entity.id'))
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('elec_candidate.id'))
    votes: Mapped[int] = mapped_column(Integer, nullable=True)
    vote_percentage: Mapped[float] = mapped_column(Float, nullable=True)
    rank: Mapped[int] = mapped_column(Integer, nullable=True)
