# LokTathya Source Access Policy

This policy governs the access pathways used by LokTathya's Fetch Orchestrator to interact with official government domains.

---

## 1. Domain Scope Verification
The Controlled Discovery Engine and ResilientHTTPClient are locked to specific domain patterns verified by the Source Registry:
- Scrapers and fetch tasks may only issue requests to domains matching the `official_domain` or subdomains explicitly whitelisted for a registered `Source`.
- Wildcard crawling outside registered official scopes is prohibited.

---

## 2. SSRF Protection Protocols
Every URL undergoes validation prior to socket opening:
- IP Resolution: The hostnames are resolved recursively to confirm the target does not belong to private IPv4/IPv6 ranges (e.g. RFC 1918 subnets, Docker service networks).
- Port Limits: Only port 80 (HTTP) and port 443 (HTTPS) connections are allowed.
- Redirect Verification: Redirect headers are captured, and the target redirect URL is recursively validated against the SSRF filter before following.

---

## 3. Robots.txt Compliance
- Scrapers retrieve the `robots.txt` configuration from the target root domain.
- Ingestion tasks respect the `Crawl-delay` and `Disallow` rules declared by the official authority.
- Custom user-agent signatures (e.g. `LokTathyaBot/1.0`) are sent in request headers for audit transparency.

---

## 4. Anti-bot and Circumvention Limits
- LokTathya does NOT bypass anti-bot challenges (CAPTCHAs, Cloudflare protection walls, login forms).
- If an official endpoint requires credentials, they must be registered securely using Vault environment storage.
- If a target endpoint blocks requests, the source status is degraded to `BLOCKED` in the database, and ingestion stops until human operators review the access terms.
