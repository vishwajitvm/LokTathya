import httpx
import logging
from typing import Optional, Dict, Any
from urllib.parse import urlparse
import ipaddress

logger = logging.getLogger(__name__)

class ResilientHTTPClient:
    """
    A reusable HTTP client service for LokTathya.
    Supports timeouts, connection pooling, redirect limits, and basic SSRF protection.
    """

    def __init__(self, timeout: int = 15, max_redirects: int = 3):
        self.timeout = timeout
        self.max_redirects = max_redirects
        self.client = httpx.AsyncClient(
            timeout=self.timeout,
            follow_redirects=True,
            max_redirects=self.max_redirects
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
        Fetch a resource conditionally.
        """
        if not self._is_safe_url(url):
            return {"status": "BLOCKED", "error": "Unsafe URL (SSRF Prevention)"}

        headers = {}
        if etag:
            headers["If-None-Match"] = etag
        if last_modified:
            headers["If-Modified-Since"] = last_modified

        try:
            response = await self.client.request(method, url, headers=headers)
            
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
