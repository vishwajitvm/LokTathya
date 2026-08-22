import json
import csv
import io
from typing import Dict, Any, List, Optional
try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

try:
    import openpyxl
except ImportError:
    openpyxl = None

from ingestion.html_normalizer import HTMLNormalizer
from core.format_detector import FormatDetector

class ParserFactory:
    """
    Priority 1: Multi-format parsing factory for HTML, PDF, CSV, XLSX, JSON.
    Conforms to a strict, standardized output model.
    """

    @staticmethod
    def get_parser(detected_format: str):
        if detected_format == "HTML":
            return HTMLParser()
        elif detected_format == "PDF":
            return PDFParser()
        elif detected_format == "CSV":
            return CSVParser()
        elif detected_format == "XLSX":
            return XLSXParser()
        elif detected_format == "JSON":
            return JSONParser()
        else:
            raise NotImplementedError(f"No parser implemented for format: {detected_format}")

class BaseParser:
    def parse(self, content: bytes, meta: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

    def _build_result(
        self,
        meta: Dict[str, Any],
        structured_content: Any,
        text_content: Optional[str] = None,
        parser_name: str = "Base",
        parser_version: str = "1.0.0",
        status: str = "SUCCESS"
    ) -> Dict[str, Any]:
        return {
            "document_id": meta.get("document_id"),
            "version_id": meta.get("version_id"),
            "source_id": meta.get("source_id"),
            "parser_name": parser_name,
            "parser_version": parser_version,
            "status": status,
            "metadata": meta.get("custom_metadata", {}),
            "structured_content": structured_content,
            "text_content": text_content,
            "extraction_location": meta.get("storage_path", "unknown")
        }

class HTMLParser(BaseParser):
    def parse(self, content: bytes, meta: Dict[str, Any]) -> Dict[str, Any]:
        html_str = content.decode('utf-8', errors='ignore')
        normalizer = HTMLNormalizer(html_str)
        norm_res = normalizer.normalize()
        tables = normalizer.extract_tables()
        
        # Link extraction
        from ingestion.link_extractor import DocumentLinkExtractor
        extractor = DocumentLinkExtractor(html_str, meta.get("base_url", "https://gov.in"))
        links = extractor.extract_links()

        structured = {
            "tables": tables,
            "links": links,
            "title": norm_res.get("title")
        }

        return self._build_result(
            meta=meta,
            structured_content=structured,
            text_content=norm_res["text"],
            parser_name="HTMLParser"
        )

class PDFParser(BaseParser):
    def parse(self, content: bytes, meta: Dict[str, Any]) -> Dict[str, Any]:
        text_runs = []
        page_count = 0
        if PdfReader:
            try:
                reader = PdfReader(io.BytesIO(content))
                page_count = len(reader.pages)
                for page in reader.pages:
                    txt = page.extract_text() or ""
                    text_runs.append(txt)
            except Exception as e:
                return self._build_result(meta=meta, structured_content={}, status=f"ERROR: {str(e)}", parser_name="PDFParser")
        else:
            text_runs.append("pypdf missing in runtime environment")

        full_text = "\n--- PAGE BREAK ---\n".join(text_runs)
        
        return self._build_result(
            meta=meta,
            structured_content={"page_count": page_count},
            text_content=full_text,
            parser_name="PDFParser"
        )

class CSVParser(BaseParser):
    def parse(self, content: bytes, meta: Dict[str, Any]) -> Dict[str, Any]:
        # Detect encoding
        encoding = FormatDetector._detect_csv_encoding(content)
        csv_str = content.decode(encoding, errors='ignore')
        
        # Detect delimiter
        dialect = None
        try:
            dialect = csv.Sniffer().sniff(csv_str[:4096])
        except Exception:
            pass
            
        delimiter = dialect.delimiter if dialect else ','
        
        rows = []
        reader = csv.reader(io.StringIO(csv_str), delimiter=delimiter)
        for row in reader:
            rows.append(row)
            
        headers = rows[0] if rows else []
        data_rows = rows[1:] if len(rows) > 1 else []

        structured = {
            "headers": headers,
            "rows": data_rows,
            "delimiter": delimiter,
            "encoding": encoding
        }
        
        return self._build_result(
            meta=meta,
            structured_content=structured,
            text_content=csv_str,
            parser_name="CSVParser"
        )

class XLSXParser(BaseParser):
    def parse(self, content: bytes, meta: Dict[str, Any]) -> Dict[str, Any]:
        sheets = {}
        if openpyxl:
            try:
                wb = openpyxl.load_workbook(io.BytesIO(content), data_only=True)
                for sheet_name in wb.sheetnames:
                    ws = wb[sheet_name]
                    sheet_rows = []
                    for row in ws.iter_rows(values_only=True):
                        # Convert cells to string or primitives
                        sheet_rows.append([str(cell) if cell is not None else "" for cell in row])
                    sheets[sheet_name] = {
                        "headers": sheet_rows[0] if sheet_rows else [],
                        "rows": sheet_rows[1:] if len(sheet_rows) > 1 else []
                    }
            except Exception as e:
                return self._build_result(meta=meta, structured_content={}, status=f"ERROR: {str(e)}", parser_name="XLSXParser")
        else:
            sheets["error"] = "openpyxl missing in environment"

        return self._build_result(
            meta=meta,
            structured_content={"sheets": sheets},
            text_content=json.dumps(sheets, indent=2),
            parser_name="XLSXParser"
        )

class JSONParser(BaseParser):
    def parse(self, content: bytes, meta: Dict[str, Any]) -> Dict[str, Any]:
        try:
            data = json.loads(content.decode('utf-8', errors='ignore'))
        except Exception as e:
            return self._build_result(meta=meta, structured_content={}, status=f"ERROR: {str(e)}", parser_name="JSONParser")

        return self._build_result(
            meta=meta,
            structured_content=data,
            text_content=json.dumps(data, indent=2),
            parser_name="JSONParser"
        )
