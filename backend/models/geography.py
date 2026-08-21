from sqlalchemy import Column, String, Integer, ForeignKey, Date, DateTime, Boolean, CheckConstraint, Index
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, JSONB
from geoalchemy2 import Geometry
from .base import Base
import uuid
from datetime import datetime

class Geography(Base):
    __tablename__ = 'geo_entity'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type: Mapped[str] = mapped_column(String(50), index=True) # Country, State, District, Subdistrict, Block, Village, GramPanchayat, Municipality, Ward, Constituency
    name: Mapped[str] = mapped_column(String(255))
    geom = Column(Geometry('MULTIPOLYGON', srid=4326))
    geom_simplified = Column(Geometry('MULTIPOLYGON', srid=4326), nullable=True) # For map rendering
    valid_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    valid_until: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        CheckConstraint('valid_until >= valid_from', name='check_valid_dates_geo'),
    )

class GeoRelationship(Base):
    __tablename__ = 'geo_relationship'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    parent_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('geo_entity.id'))
    child_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('geo_entity.id'))
    relationship_type: Mapped[str] = mapped_column(String(50), index=True) # ADMINISTRATIVE, ELECTORAL, SUPERSEDES
    valid_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    valid_until: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        CheckConstraint('valid_until >= valid_from', name='check_valid_dates_rel'),
    )
