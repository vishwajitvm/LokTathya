# LokTathya Rate Limiting & Crawl Delay Policy

This policy governs the throttling limits applied to outbound fetch operations and inbound API queries to maintain platform stability.

---

## 1. Outbound Request Throttling
- The Fetch Orchestrator uses a Redis-backed rate limiter to enforce delays between requests to target domains.
- The default limit is 1 request per 3 seconds per host.
- For high-priority sources during budget releases, the delay can be customized, but it must never be lower than 1 request per 1 second to avoid trigger-blocking rules on target portals.

---

## 2. Exponential Backoff and Retries
When an HTTP request returns transient errors (e.g. 429 Too Many Requests, 503 Service Unavailable), LokTathya applies:
- Exponential backoff: delay doubles after every retry.
- Jitter: random noise (+/- 200ms) is added to delay intervals to prevent thundering herds.
- Max retries: limited to 3 attempts. If all attempts fail, the endpoint is marked `DEGRADED`.

---

## 3. Inbound API Rate Limits
To prevent service exhaustion, the public FastAPI service implements rate limiting:
- Anonymous Requests: Bounded to 60 requests per minute per IP.
- Authenticated/Developer Requests: Bounded to 500 requests per minute.
- Responses returning HTTP 429 Too Many Requests include standard `Retry-After` headers.

---

## 4. Resource Allocation
- Large file downloads (e.g. PDF/XLSX attachments > 50MB) are routed to a slow execution queue.
- Celery worker queues use thread-pool limits to guarantee that heavy parsing runs do not exhaust CPU cycles on the host.
