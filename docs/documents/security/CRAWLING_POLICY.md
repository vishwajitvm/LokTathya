# LokTathya Crawling & Discovery Policy

This document regulates URL link discovery and automated sitemap scrapers inside LokTathya.

---

## 1. Discovery Scope
Automated discovery is only executed on registered official endpoints. The engine is divided into three levels:
- **Sitemap Index Parser**: Reads xml sitemaps to fetch absolute URLs.
- **RSS/Atom Feed Scraper**: Captures recently added press releases and circulars.
- **HTML Link Collector**: Parses page bodies and extracts outbound document links (PDFs, CSVs) or sub-section pages.

---

## 2. Limits and Backoff Heuristics
To prevent hitting official servers, the following crawling parameters are enforced:
- **Max Crawl Depth**: 2 (restricted to the main page and immediate document attachments or lists).
- **Rate Limit**: Maximum of 1 request per 3 seconds per target domain.
- **Max Pages**: Bounded to 50 pages per discovery run task.
- **Concurreny**: discovery runs are executed in a single-threaded queue.

---

## 3. Redirect Handling
- Safe redirect resolution is enabled up to 3 hops.
- Redirect chains are analyzed to prevent infinite redirect loops.
- Any redirect that leads to an external domain not registered in the Source Registry triggers alert notifications and halts processing.

---

## 4. Ingestion Triggers
- When a new document URL is discovered, it is not ingested immediately.
- It is registered as a `Candidate` in the database.
- Celery worker pulls candidates periodically, checks their headers (ETag/Last-Modified), and schedules them for ingestion based on source priorities.
