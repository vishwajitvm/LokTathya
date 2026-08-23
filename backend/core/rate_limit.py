import os
import time
import asyncio
import redis.asyncio as redis
from urllib.parse import urlparse

class DomainRateLimiter:
    def __init__(self, redis_url: str = None):
        self.redis_url = redis_url or os.environ.get("REDIS_URL", "redis://redis:6379/0")
        self.client = redis.from_url(self.redis_url)
        # Default limits
        self.DEFAULT_RPM = 60  # 60 requests per minute per domain
        
    async def wait_if_needed(self, url: str, rpm: int = None):
        """
        Enforce rate limits per domain using a rolling window or token bucket in Redis.
        We will use a simple fixed-window approach for the prototype scale.
        """
        parsed = urlparse(url)
        domain = parsed.hostname
        if not domain:
            return
            
        limit = rpm if rpm is not None else self.DEFAULT_RPM
        if limit <= 0:
            return  # No limit
            
        key = f"ratelimit:domain:{domain}"
        
        while True:
            # Atomic increment
            current = await self.client.incr(key)
            if current == 1:
                # Set expiry on first request in the window
                await self.client.expire(key, 60)
                break
            elif current <= limit:
                break
            else:
                # We exceeded the limit for this minute.
                # Wait a bit and retry.
                await asyncio.sleep(1.0)
                
    async def close(self):
        await self.client.close()
