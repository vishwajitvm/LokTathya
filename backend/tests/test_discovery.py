import pytest
import asyncio
from unittest.mock import patch, MagicMock
from ingestion.discovery import ControlledDiscoveryEngine

@pytest.mark.anyio
async def test_discovery_sitemap():
    sitemap_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url><loc>https://example.gov.in/page1.html</loc></url>
        <url><loc>https://example.gov.in/page2.html</loc></url>
    </urlset>"""
    
    engine = ControlledDiscoveryEngine(allowed_domains={"example.gov.in"})
    
    # Mock http fetch response
    mock_res = {
        "status": "SUCCESS",
        "status_code": 200,
        "content": sitemap_xml
    }
    
    with patch("core.http_client.ResilientHTTPClient.fetch", return_value=mock_res):
        urls = await engine.discover_sitemap("https://example.gov.in/sitemap.xml")
        assert len(urls) == 2
        assert "https://example.gov.in/page1.html" in urls

@pytest.mark.anyio
async def test_discovery_rss():
    rss_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
        <channel>
            <item><link>https://example.gov.in/press/1</link></item>
            <item><link>https://external.com/spam</link></item>
        </channel>
    </rss>"""
    
    engine = ControlledDiscoveryEngine(allowed_domains={"example.gov.in"})
    mock_res = {
        "status": "SUCCESS",
        "content": rss_xml
    }
    
    with patch("core.http_client.ResilientHTTPClient.fetch", return_value=mock_res):
        urls = await engine.discover_rss("https://example.gov.in/feed.xml")
        # should filter out external.com
        assert len(urls) == 1
        assert urls[0] == "https://example.gov.in/press/1"
