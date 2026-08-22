import pytest
import zipfile
import io
from ingestion.parser_factory import ParserFactory

def test_zip_decompression_bomb_rejection():
    # Build in-memory zip file with fake large size info (simulating a decompressed bomb)
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as z:
        # Create a tiny file but with infolist modification or multiple entries
        for i in range(1001):
            z.writestr(f"file_{i}.txt", "data")
            
    parser = ParserFactory.get_parser("ZIP")
    res = parser.parse(zip_buffer.getvalue(), {"document_id": "test", "detected_format": "ZIP"})
    assert "too many files" in res["status"]

def test_pdf_page_limit_rejection():
    from pypdf import PdfWriter
    writer = PdfWriter()
    # Add 501 blank pages to trigger the limit check
    for _ in range(501):
        writer.add_blank_page(width=72, height=72)
        
    pdf_bytes = io.BytesIO()
    writer.write(pdf_bytes)
    
    parser = ParserFactory.get_parser("PDF")
    res = parser.parse(pdf_bytes.getvalue(), {"document_id": "test"})
    assert "page count exceeds" in res["status"]

def test_csv_file_size_rejection():
    # Create large CSV buffer (>50MB)
    large_csv = b"a,b,c\n" * (10 * 1024 * 1024) # ~60MB
    parser = ParserFactory.get_parser("CSV")
    res = parser.parse(large_csv, {"document_id": "test"})
    assert "exceeds maximum limit" in res["status"]
