import hashlib
import uuid
import time
from sqlalchemy.orm import Session
from models.source import ContentVersion, Document
from ingestion.diff_engine import DocumentDiffEngine

class PDFProcessor:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.diff_engine = DocumentDiffEngine()

    def process_pdf(self, file_path: str, document_id: uuid.UUID) -> dict:
        """
        Process a PDF, handling deduplication based on content hash.
        """
        # Read and hash the PDF
        with open(file_path, 'rb') as f:
            content = f.read()
        
        file_hash = hashlib.sha256(content).hexdigest()
        byte_size = len(content)

        # Check if this content version already exists for this document
        existing_version = self.db.query(ContentVersion).filter_by(
            document_id=document_id,
            sha256=file_hash
        ).first()

        if existing_version:
            return {
                "status": "UNCHANGED",
                "content_version_id": existing_version.id,
                "message": "Content hash matched existing version."
            }
        
        # Determine the new version number
        latest_version = self.db.query(ContentVersion).filter_by(
            document_id=document_id
        ).order_by(ContentVersion.version_number.desc()).first()

        new_version_num = (latest_version.version_number + 1) if latest_version else 1

        # Save new content version
        new_version = ContentVersion(
            document_id=document_id,
            version_number=new_version_num,
            sha256=file_hash,
            byte_size=byte_size,
            mime_type="application/pdf"
            # page_count could be extracted here via PyPDF2
        )
        self.db.add(new_version)
        self.db.commit()

        # Generate Diff if previous version exists
        diff_result = None
        if latest_version:
            # Here we would load extracted text for both versions and diff them
            diff_result = self.diff_engine.diff_documents({}, {}) # Mock objects

        return {
            "status": "NEW_VERSION",
            "content_version_id": new_version.id,
            "version_number": new_version_num,
            "diff": diff_result
        }


class OCRProvider:
    def extract_text(self, file_path: str):
        raise NotImplementedError

class TesseractProvider(OCRProvider):
    def extract_text(self, file_path: str):
        start = time.time()
        # Mock OCR extraction
        time.sleep(0.1) 
        duration = time.time() - start
        return {
            "text": "mock extracted text from tesseract",
            "confidence": 0.85,
            "duration": duration,
            "engine": "tesseract",
            "version": "5.3.0"
        }

class PDFChunker:
    def chunk(self, text: str, document_id: str, version_id: str):
        # Mock chunking
        return [{
            "chunk_id": str(uuid.uuid4()),
            "document_id": document_id,
            "content_version_id": version_id,
            "page_number": 1,
            "chunk_index": 0,
            "text": text[:500],
            "token_count": len(text.split())
        }]
