# API CAPABILITY MATRIX

| CAPABILITY | CURRENT | MISSING | REQUIRED | STATUS |
|------------|---------|---------|----------|--------|
| Public / Internal | Single router | RBAC / Auth layer | Security isolation | MISSING |
| Pagination | Limit/Offset | Cursor pagination for >1M rows | Keyset pagination | PARTIAL |
| Async Jobs | Synchronous | 202 Accepted + Job ID | Celery job tracker APIs | MISSING |
| SSRF Protect | None | Block local/internal IPs | URL Validator | MISSING |
| Traceability | request_id | Injecting into DB records | Middleware TraceNest | PARTIAL |
| Cache | None | Redis layer for static/public data | Redis Cache | MISSING |
