import httpx
import logging
from typing import Optional, Dict, Any
from urllib.parse import urlparse, urljoin
import ipaddress

logger = logging.getLogger(__name__)

class ResilientHTTPClient:
    """
    A reusable HTTP client service for LokTathya.
    Supports timeouts, connection pooling, redirect limits, and manual redirect SSRF checks.
    """

    def __init__(self, timeout: int = 15, max_redirects: int = 3):
        self.timeout = timeout
        self.max_redirects = max_redirects
        self.client = httpx.AsyncClient(
            timeout=self.timeout,
            follow_redirects=False
        )

    def _is_safe_url(self, url: str) -> bool:
        """Basic SSRF protection: prevent accessing internal IPs."""
        parsed = urlparse(url)
        if not parsed.hostname:
            return False
        try:
            ip = ipaddress.ip_address(parsed.hostname)
            if ip.is_private or ip.is_loopback:
                return False
        except ValueError:
            # Not an IP, likely a domain. DNS resolution is needed for strict SSRF,
            # but we assume the network layer/DNS blocks internal domains.
            if parsed.hostname in ['localhost', '127.0.0.1']:
                return False
        return True

    async def fetch(
        self,
        url: str,
        etag: Optional[str] = None,
        last_modified: Optional[str] = None,
        method: str = "GET"
    ) -> Dict[str, Any]:
        """
        Fetch a resource conditionally with manual redirect check.
        """
        current_url = url
        redirect_count = 0
        headers = {}
        if etag:
            headers["If-None-Match"] = etag
        if last_modified:
            headers["If-Modified-Since"] = last_modified

        while True:
            if not self._is_safe_url(current_url):
                return {"status": "BLOCKED", "error": "Unsafe URL (SSRF Prevention)"}

            try:
                response = await self.client.request(method, current_url, headers=headers)
                
                # Check for redirects
                if response.status_code in (301, 302, 303, 307, 308):
                    redirect_count += 1
                    if redirect_count > self.max_redirects:
                        return {"status": "HTTP_ERROR", "error": "Too many redirects"}
                    
                    location = response.headers.get("Location")
                    if not location:
                        return {"status": "HTTP_ERROR", "error": "Redirect header missing Location"}
                    
                    current_url = urljoin(current_url, location)
                    continue

                if response.status_code == 304:
                    return {"status": "NOT_MODIFIED", "status_code": 304}

                response.raise_for_status()

                return {
                    "status": "SUCCESS",
                    "status_code": response.status_code,
                    "content": response.content,
                    "headers": dict(response.headers),
                    "url": str(response.url)
                }

            except httpx.HTTPStatusError as e:
                return {"status": "HTTP_ERROR", "status_code": e.response.status_code, "error": str(e)}
            except httpx.RequestError as e:
                return {"status": "NETWORK_ERROR", "error": str(e)}
            except Exception as e:
                return {"status": "UNKNOWN_ERROR", "error": str(e)}

    async def close(self):
        await self.client.aclose()
