from ingestion.link_extractor import DocumentLinkExtractor

def test_extract_pdf_link():
    html = '<html><body><a href="/docs/budget.pdf">Download Budget</a></body></html>'
    extractor = DocumentLinkExtractor(html, "https://gov.in")
    links = extractor.extract_links()
    assert len(links) == 1
    assert links[0]["url"] == "https://gov.in/docs/budget.pdf"
    assert links[0]["type"] == "PDF"
    assert links[0]["text"] == "Download Budget"

def test_extract_csv_with_query():
    html = '<html><body><a href="https://data.gov.in/export.csv?id=123">Export Data</a></body></html>'
    extractor = DocumentLinkExtractor(html, "https://gov.in")
    links = extractor.extract_links()
    assert len(links) == 1
    assert links[0]["type"] == "CSV"

def test_ignore_javascript():
    html = '<html><body><a href="javascript:void(0)">Click</a><a href="/api/v1/data.json">Data</a></body></html>'
    extractor = DocumentLinkExtractor(html, "https://gov.in")
    links = extractor.extract_links()
    assert len(links) == 1
    assert links[0]["type"] == "API"
    assert links[0]["url"] == "https://gov.in/api/v1/data.json"
