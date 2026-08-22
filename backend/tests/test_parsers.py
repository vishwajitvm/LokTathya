import pytest
from ingestion.parser_factory import ParserFactory
import json
import io

def test_html_parser():
    html_content = b"<html><head><title>Test</title></head><body><h1>Budget Report</h1><table><tr><th>Year</th><th>Spent</th></tr><tr><td>2026</td><td>10</td></tr></table><a href='/docs/budget.pdf'>Download</a></body></html>"
    meta = {
        "document_id": "doc-1",
        "version_id": "v-1",
        "source_id": "src-1",
        "storage_path": "raw/test.html",
        "base_url": "https://gov.in"
    }
    
    parser = ParserFactory.get_parser("HTML")
    res = parser.parse(html_content, meta)
    
    assert res["status"] == "SUCCESS"
    assert "Budget Report" in res["text_content"]
    assert res["structured_content"]["title"] == "Test"
    assert len(res["structured_content"]["tables"]) == 1
    assert res["structured_content"]["tables"][0]["headers"] == ["Year", "Spent"]
    assert res["structured_content"]["tables"][0]["rows"] == [["2026", "10"]]
    
    links = res["structured_content"]["links"]
    assert len(links) == 1
    assert links[0]["url"] == "https://gov.in/docs/budget.pdf"
    assert links[0]["type"] == "PDF"

def test_pdf_parser():
    from pypdf import PdfWriter
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    
    pdf_bytes = io.BytesIO()
    writer.write(pdf_bytes)
    pdf_content = pdf_bytes.getvalue()
    
    meta = {"document_id": "doc-2", "version_id": "v-1"}
    parser = ParserFactory.get_parser("PDF")
    res = parser.parse(pdf_content, meta)
    
    assert res["parser_name"] == "PDFParser"
    assert res["structured_content"]["page_count"] == 1

def test_csv_parser():
    csv_content = b"Item,Cost\nApple,10\nBanana,12"
    meta = {"document_id": "doc-3"}
    
    parser = ParserFactory.get_parser("CSV")
    res = parser.parse(csv_content, meta)
    
    assert res["status"] == "SUCCESS"
    assert res["structured_content"]["headers"] == ["Item", "Cost"]
    assert res["structured_content"]["rows"] == [["Apple", "10"], ["Banana", "12"]]

def test_json_parser():
    json_content = json.dumps({"status": "active", "count": 100}).encode('utf-8')
    meta = {"document_id": "doc-4"}
    
    parser = ParserFactory.get_parser("JSON")
    res = parser.parse(json_content, meta)
    
    assert res["status"] == "SUCCESS"
    assert res["structured_content"]["status"] == "active"
    assert res["structured_content"]["count"] == 100

def test_xlsx_parser():
    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Sheet1"
    ws.append(["Header1", "Header2"])
    ws.append(["Val1", "Val2"])
    
    xlsx_bytes = io.BytesIO()
    wb.save(xlsx_bytes)
    xlsx_content = xlsx_bytes.getvalue()
    
    meta = {"document_id": "doc-5"}
    parser = ParserFactory.get_parser("XLSX")
    res = parser.parse(xlsx_content, meta)
    
    assert res["status"] == "SUCCESS"
    sheets = res["structured_content"]["sheets"]
    assert "Sheet1" in sheets
    assert sheets["Sheet1"]["headers"] == ["Header1", "Header2"]
    assert sheets["Sheet1"]["rows"] == [["Val1", "Val2"]]
