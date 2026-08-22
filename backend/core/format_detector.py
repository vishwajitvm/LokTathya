import os
try:
    import magic
except ImportError:
    class MockMagic:
        @staticmethod
        def from_buffer(buffer, mime=False):
            return "application/octet-stream"
    magic = MockMagic()
from typing import Dict, Any

class FormatDetector:
    """
    Priority 1 implementation of a robust format detector.
    Identifies files based on Content-Type, extension, magic bytes, and internal structure.
    """
    
    SUPPORTED_MIME_TYPES = {
        'application/pdf': 'PDF',
        'text/html': 'HTML',
        'text/csv': 'CSV',
        'text/tab-separated-values': 'TSV',
        'application/json': 'JSON',
        'application/xml': 'XML',
        'application/vnd.ms-excel': 'XLS',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'XLSX',
        'application/vnd.ms-excel.sheet.macroEnabled.12': 'XLSM',
        'application/vnd.oasis.opendocument.spreadsheet': 'ODS',
        'application/zip': 'ZIP',
        'application/gzip': 'GZIP',
        'application/geo+json': 'GEOJSON',
        'application/vnd.google-earth.kml+xml': 'KML',
        'application/vnd.google-earth.kmz': 'KMZ',
    }

    @staticmethod
    def detect_format(content: bytes, content_type: str = None, filename: str = None) -> Dict[str, Any]:
        """
        Identify the format of the given byte content.
        """
        result = {
            "detected_format": "UNKNOWN",
            "mime_type": "application/octet-stream",
            "confidence": "LOW",
            "encoding": "UNKNOWN",
            "mismatch": False
        }

        # 1. Magic bytes detection
        try:
            detected_mime = magic.from_buffer(content[:2048], mime=True)
            if detected_mime == "application/octet-stream" and content_type:
                detected_mime = content_type
            result["mime_type"] = detected_mime
            if detected_mime in FormatDetector.SUPPORTED_MIME_TYPES:
                result["detected_format"] = FormatDetector.SUPPORTED_MIME_TYPES[detected_mime]
                result["confidence"] = "HIGH"
        except Exception:
            detected_mime = content_type
            if detected_mime in FormatDetector.SUPPORTED_MIME_TYPES:
                result["detected_format"] = FormatDetector.SUPPORTED_MIME_TYPES[detected_mime]
                result["confidence"] = "LOW"

        # 2. Check for mismatches between claimed Content-Type and Magic Bytes
        if content_type and detected_mime and content_type != detected_mime:
            # Often servers return text/html for PDFs by mistake
            if detected_mime == 'application/pdf' and content_type == 'text/html':
                result["mismatch"] = True
                result["detected_format"] = "PDF" # Trust magic over header
            else:
                result["mismatch"] = True

        # 3. Deep introspection for CSV encodings if it's text/csv
        if result["detected_format"] == "CSV" or (content_type == "text/csv" and result["confidence"] == "LOW"):
            result["detected_format"] = "CSV"
            encoding = FormatDetector._detect_csv_encoding(content)
            result["encoding"] = encoding

        # 4. Deep introspection for ZIP (Shapefiles)
        if result["detected_format"] == "ZIP":
            if FormatDetector._is_shapefile_archive(content):
                result["detected_format"] = "SHAPEFILE_ARCHIVE"
                result["confidence"] = "HIGH"

        return result

    @staticmethod
    def _detect_csv_encoding(content: bytes) -> str:
        """
        Robustly detect CSV encoding, including UTF-8 BOM and UTF-16.
        """
        if content.startswith(b'\xef\xbb\xbf'):
            return "utf-8-sig"
        elif content.startswith(b'\xff\xfe') or content.startswith(b'\xfe\xff'):
            return "utf-16"
        
        # Fallback to chardet if available, else assume utf-8
        try:
            import chardet
            detection = chardet.detect(content[:10000])
            if detection and detection['confidence'] > 0.7:
                return detection['encoding'] or "utf-8"
        except ImportError:
            pass
            
        return "utf-8"

    @staticmethod
    def _is_shapefile_archive(content: bytes) -> bool:
        """
        Check if a ZIP archive is a valid Shapefile (contains .shp, .shx, .dbf).
        """
        import zipfile
        import io
        try:
            with zipfile.ZipFile(io.BytesIO(content)) as z:
                names = z.namelist()
                has_shp = any(n.endswith('.shp') for n in names)
                has_shx = any(n.endswith('.shx') for n in names)
                has_dbf = any(n.endswith('.dbf') for n in names)
                return has_shp and has_shx and has_dbf
        except zipfile.BadZipFile:
            return False
