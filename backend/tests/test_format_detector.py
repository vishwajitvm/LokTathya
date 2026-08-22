import pytest
import io
import zipfile
from core.format_detector import FormatDetector

def test_csv_encoding_utf8_bom():
    content = b'\xef\xbb\xbfName,Age\nJohn,30'
    res = FormatDetector.detect_format(content, content_type='text/csv')
    assert res["detected_format"] == "CSV"
    assert res["encoding"] == "utf-8-sig"

def test_csv_encoding_utf16():
    content = b'\xff\xfeN\x00a\x00m\x00e\x00,\x00A\x00g\x00e\x00\n\x00'
    res = FormatDetector.detect_format(content, content_type='text/csv')
    assert res["detected_format"] == "CSV"
    assert res["encoding"] == "utf-16"

def test_shapefile_detection():
    # Create an in-memory zip file simulating a shapefile
    mem_zip = io.BytesIO()
    with zipfile.ZipFile(mem_zip, mode="w") as zf:
        zf.writestr("test.shp", b"dummy")
        zf.writestr("test.shx", b"dummy")
        zf.writestr("test.dbf", b"dummy")
        zf.writestr("test.prj", b"dummy")
    
    zip_bytes = mem_zip.getvalue()
    
    res = FormatDetector.detect_format(zip_bytes, content_type='application/zip')
    assert res["detected_format"] == "SHAPEFILE_ARCHIVE"
    assert res["confidence"] == "HIGH"

def test_regular_zip_detection():
    mem_zip = io.BytesIO()
    with zipfile.ZipFile(mem_zip, mode="w") as zf:
        zf.writestr("test.txt", b"dummy text")
        
    zip_bytes = mem_zip.getvalue()
    
    res = FormatDetector.detect_format(zip_bytes, content_type='application/zip')
    assert res["detected_format"] == "ZIP"
    assert res["confidence"] == "HIGH"
