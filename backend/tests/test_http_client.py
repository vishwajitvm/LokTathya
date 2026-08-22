import pytest
import asyncio
from core.http_client import ResilientHTTPClient

def test_ssrf_protection_localhost():
    client = ResilientHTTPClient()
    res = asyncio.run(client.fetch("http://localhost:8000/admin"))
    assert res["status"] == "BLOCKED"

def test_ssrf_protection_127():
    client = ResilientHTTPClient()
    res = asyncio.run(client.fetch("http://127.0.0.1/server-status"))
    assert res["status"] == "BLOCKED"

def test_ssrf_protection_private_ip():
    client = ResilientHTTPClient()
    res = asyncio.run(client.fetch("http://192.168.1.100/internal"))
    assert res["status"] == "BLOCKED"

def test_http_conditional_fetch(monkeypatch):
    client = ResilientHTTPClient()
    
    # Mock httpx client response
    class MockResponse:
        status_code = 304
        headers = {}
        content = b""
        url = "http://example.gov.in/data.json"
        def raise_for_status(self):
            pass

    async def mock_request(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(client.client, 'request', mock_request)
    
    res = asyncio.run(client.fetch("http://example.gov.in/data.json", etag="W/12345"))
    assert res["status"] == "NOT_MODIFIED"
    assert res["status_code"] == 304
