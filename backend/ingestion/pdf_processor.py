class OCRProvider:
    def extract_text(self, file_path: str):
        raise NotImplementedError

class TesseractProvider(OCRProvider):
    def extract_text(self, file_path: str):
        import time
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
