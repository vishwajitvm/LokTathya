# Phase 7 Access Policy & robots.txt Compliance

This document details user-agent policies and crawl limitations.

---

## 1. Compliance Controls
- Checks target `robots.txt` paths for disallow patterns matching `LokTathyaBot`.
- Restricts scraping speed using parsed crawl-delay parameters.
- Disallowed endpoints or those missing explicit public license terms are flagged as `REQUIRES_REVIEW` and not fetched.
