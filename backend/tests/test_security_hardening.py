import pytest
import asyncio
import zipfile
import io
from unittest.mock import patch
from core.http_client import ResilientHTTPClient
from ingestion.parser_factory import ParserFactory

@pytest.mark.anyio
async def test_redirect_ssrf_blocking():
    client = ResilientHTTPClient()
    # Mocking first hop redirect to an unsafe location
    mock_res_redirect = MagicMock()
    mock_res_redirect.status_code = 302
    mock_res_redirect.headers = {"Location": "http://127.0.0.1/admin"}
    
    with patch.object(client.client, "request", return_value=mock_res_redirect):
        res = await client.fetch("https://safe-domain.com/start-redirect")
        # Should follow to 127.0.0.1, check resolved host safety, and block
        assert res["status"] == "BLOCKED"
        assert "SSRF" in res["error"]

def test_xml_xxe_rejection():
    xxe_xml = b"""<?xml version="1.0" encoding="ISO-8859-1"?>
    <!DOCTYPE foo [  
      <!ELEMENT foo ANY >
      <!ENTITY xxe SYSTEM "file:///etc/passwd" >]>
    <foo>&xxe;</foo>"""
    
    parser = ParserFactory.get_parser("XML")
    res = parser.parse(xxe_xml, {"document_id": "test"})
    assert "forbidden" in res["status"]

def test_xml_billion_laughs_rejection():
    billion_laughs = b"""<?xml version="1.0"?>
    <!DOCTYPE lolz [
     <!ENTITY lol "lol">
     <!ENTITY lol1 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
    ]>
    <lolz>&lol1;</lolz>"""
    
    parser = ParserFactory.get_parser("XML")
    res = parser.parse(billion_laughs, {"document_id": "test"})
    assert "forbidden" in res["status"]

def test_zip_slip_rejection():
    # Generate in-memory zip file containing a traversal file name
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as z:
        z.writestr("../traversal.txt", "payload")
        
    parser = ParserFactory.get_parser("ZIP")
    res = parser.parse(zip_buffer.getvalue(), {"document_id": "test", "detected_format": "ZIP"})
    assert "Zip Slip" in res["status"]

class MagicMock:
    pass
