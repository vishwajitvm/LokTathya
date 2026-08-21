from sqlalchemy import Column, String, Integer, ForeignKey, Date, DateTime, Boolean, Numeric, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, JSONB
from geoalchemy2 import Geometry
from .base import Base
import uuid
from datetime import datetime

class Country(Base):
    __tablename__ = 'geo_country'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    code: Mapped[str] = mapped_column(String(10), unique=True)
    geom = Column(Geometry('MULTIPOLYGON', srid=4326))

class State(Base):
    __tablename__ = 'geo_state'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    country_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('geo_country.id'))
    name: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(50)) # State or Union Territory
    geom = Column(Geometry('MULTIPOLYGON', srid=4326))

class District(Base):
    __tablename__ = 'geo_district'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    state_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('geo_state.id'))
    name: Mapped[str] = mapped_column(String(255))
    geom = Column(Geometry('MULTIPOLYGON', srid=4326))
    valid_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    valid_until: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

class Constituency(Base):
    __tablename__ = 'geo_constituency'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type: Mapped[str] = mapped_column(String(50)) # Assembly, Parliamentary
    state_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('geo_state.id'))
    name: Mapped[str] = mapped_column(String(255))
    geom = Column(Geometry('MULTIPOLYGON', srid=4326))
    valid_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    valid_until: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
