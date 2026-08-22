import re
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
from typing import List, Dict, Any, Set
from core.http_client import ResilientHTTPClient
from core.url_utils import URLCanonicalizer
from ingestion.link_extractor import DocumentLinkExtractor
from tracenest import logger

class ControlledDiscoveryEngine:
    """
    Controlled Website Discovery Engine.
    Discovers sitemaps, RSS feeds, and raw HTML links under a strict domain boundary.
    """
    
    def __init__(self, allowed_domains: Set[str], max_depth: int = 2, max_pages: int = 50):
        self.allowed_domains = {d.lower() for d in allowed_domains}
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.http_client = ResilientHTTPClient()

    def _is_domain_allowed(self, url: str) -> bool:
        parsed = urlparse(url)
        if not parsed.netloc:
            return False
        netloc = parsed.netloc.lower()
        # Direct match or subdomain match
        for d in self.allowed_domains:
            if netloc == d or netloc.endswith("." + d):
                return True
        return False

    async def discover_sitemap(self, sitemap_url: str) -> List[str]:
        """Fetch and parse sitemap.xml to extract URLs."""
        if not self._is_domain_allowed(sitemap_url):
            logger.warning("Sitemap domain not allowed", url=sitemap_url)
            return []
            
        res = await self.http_client.fetch(sitemap_url)
        if res["status"] != "SUCCESS":
            return []
            
        urls = []
        try:
            root = ET.fromstring(res["content"])
            # Support namespaces
            ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            for loc in root.findall(".//ns:loc", ns):
                if loc.text:
                    urls.append(loc.text.strip())
            # Fallback if no namespace matches
            if not urls:
                for loc in root.findall(".//loc"):
                    if loc.text:
                        urls.append(loc.text.strip())
        except Exception as e:
            logger.error("Failed to parse sitemap XML", error=str(e), url=sitemap_url)
            
        return [URLCanonicalizer.canonicalize(u) for u in urls if self._is_domain_allowed(u)]

    async def discover_rss(self, rss_url: str) -> List[str]:
        """Fetch and parse RSS/Atom feed to extract URLs."""
        if not self._is_domain_allowed(rss_url):
            logger.warning("RSS domain not allowed", url=rss_url)
            return []
            
        res = await self.http_client.fetch(rss_url)
        if res["status"] != "SUCCESS":
            return []
            
        urls = []
        try:
            root = ET.fromstring(res["content"])
            # Check RSS channel items
            for link in root.findall(".//item/link"):
                if link.text:
                    urls.append(link.text.strip())
            # Check Atom entry links
            for link in root.findall(".//entry/link"):
                href = link.attrib.get("href")
                if href:
                    urls.append(href.strip())
        except Exception as e:
            logger.error("Failed to parse RSS XML", error=str(e), url=rss_url)
            
        return [URLCanonicalizer.canonicalize(u) for u in urls if self._is_domain_allowed(u)]

    async def discover_html_links(self, page_url: str) -> List[Dict[str, Any]]:
        """Fetch page and extract classified document and page links."""
        if not self._is_domain_allowed(page_url):
            logger.warning("HTML page domain not allowed", url=page_url)
            return []
            
        res = await self.http_client.fetch(page_url)
        if res["status"] != "SUCCESS":
            return []
            
        html_str = res["content"].decode('utf-8', errors='ignore')
        extractor = DocumentLinkExtractor(html_str, page_url)
        links = extractor.extract_links()
        
        # Canonicalize and filter within allowed domains
        filtered_links = []
        for l in links:
            canon_url = URLCanonicalizer.canonicalize(l["url"])
            if self._is_domain_allowed(canon_url):
                l["url"] = canon_url
                filtered_links.append(l)
                
        return filtered_links
