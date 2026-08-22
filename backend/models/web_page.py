from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Enum, JSON, Integer, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from models.base import BaseModel
import enum

class PageType(str, enum.Enum):
    HOME = "HOME"
    INDEX = "INDEX"
    LISTING = "LISTING"
    DETAIL = "DETAIL"
    ARTICLE = "ARTICLE"
    PRESS_RELEASE = "PRESS_RELEASE"
    NOTIFICATION = "NOTIFICATION"
    TENDER = "TENDER"
    BUDGET = "BUDGET"
    DATASET = "DATASET"
    DASHBOARD = "DASHBOARD"
    REPORT = "REPORT"
    POLICY = "POLICY"
    STATISTICS = "STATISTICS"
    CONTACT = "CONTACT"
    ARCHIVE = "ARCHIVE"
    UNKNOWN = "UNKNOWN"

class ChangeType(str, enum.Enum):
    NO_CHANGE = "NO_CHANGE"
    METADATA_CHANGE = "METADATA_CHANGE"
    CONTENT_CHANGE = "CONTENT_CHANGE"
    STRUCTURAL_CHANGE = "STRUCTURAL_CHANGE"
    UNKNOWN_CHANGE = "UNKNOWN_CHANGE"

class WebPage(BaseModel):
    """
    A Web Page is a first-class identity in LokTathya.
    It can be a source of truth, an index of documents, or a dataset host.
    """
    __tablename__ = 'src_web_page'

    source_id = Column(ForeignKey('src_source.id', ondelete='CASCADE'), nullable=False, index=True)
    endpoint_id = Column(ForeignKey('src_endpoint.id', ondelete='SET NULL'), nullable=True, index=True)
    
    # Canonical identity tracking
    canonical_url = Column(String(1024), nullable=False, index=True)
    current_url = Column(String(1024), nullable=False)
    
    title = Column(String(512), nullable=True)
    description = Column(Text, nullable=True)
    language = Column(String(10), nullable=True)
    
    page_type = Column(Enum(PageType), default=PageType.UNKNOWN, index=True)
    status_code = Column(Integer, nullable=True)
    
    # Temporal tracking
    published_at = Column(DateTime(timezone=True), nullable=True)
    first_seen_at = Column(DateTime(timezone=True), nullable=False)
    last_seen_at = Column(DateTime(timezone=True), nullable=False)
    last_changed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Conditional HTTP tracking
    etag = Column(String(255), nullable=True)
    last_modified = Column(String(255), nullable=True)
    
    parent_page_id = Column(ForeignKey('src_web_page.id', ondelete='SET NULL'), nullable=True)
    
    versions = relationship('WebPageVersion', back_populates='page', cascade='all, delete-orphan')

    __table_args__ = (
        UniqueConstraint('source_id', 'canonical_url', name='uq_web_page_canonical_url'),
    )

class WebPageVersion(BaseModel):
    """
    Immutable snapshots of materially changed web pages.
    """
    __tablename__ = 'src_web_page_version'
    
    page_id = Column(ForeignKey('src_web_page.id', ondelete='CASCADE'), nullable=False, index=True)
    
    version_number = Column(Integer, nullable=False)
    content_hash = Column(String(64), nullable=False, index=True)  # SHA-256 of NORMALIZED content
    raw_html_hash = Column(String(64), nullable=False)             # SHA-256 of RAW content
    
    change_type = Column(Enum(ChangeType), default=ChangeType.UNKNOWN_CHANGE)
    
    retrieved_at = Column(DateTime(timezone=True), nullable=False)
    
    storage_path = Column(String(1024), nullable=False)
    normalized_path = Column(String(1024), nullable=False)
    
    extracted_metadata = Column(JSON, default=dict)
    
    page = relationship('WebPage', back_populates='versions')
    tables = relationship('ExtractedTable', back_populates='web_version', cascade='all, delete-orphan')

class ExtractedTable(BaseModel):
    """
    Structured extraction of HTML tables from WebPages or Documents.
    """
    __tablename__ = 'src_extracted_table'
    
    web_version_id = Column(ForeignKey('src_web_page_version.id', ondelete='CASCADE'), nullable=True, index=True)
    document_version_id = Column(ForeignKey('src_content_version.id', ondelete='CASCADE'), nullable=True, index=True)
    
    table_index = Column(Integer, nullable=False)
    caption = Column(String(512), nullable=True)
    headers = Column(JSON, nullable=False)
    rows = Column(JSON, nullable=False)
    
    web_version = relationship('WebPageVersion', back_populates='tables')
