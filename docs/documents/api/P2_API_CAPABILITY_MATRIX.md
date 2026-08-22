# P2 API Capability Matrix

This matrix documents the functional status of the public API endpoints.

| Route | Method | Backing Model | Status |
| :--- | :---: | :--- | :---: |
| `/api/v1/sources/` | GET | `Source` | `PASS` |
| `/api/v1/sources/{id}` | GET | `Source` | `PASS` |
| `/api/v1/sources/{id}/endpoints` | GET | `SourceEndpoint` | `PASS` |
| `/api/v1/documents/{id}` | GET | `Document` | `PASS` |
| `/api/v1/documents/{id}/versions` | GET | `ContentVersion` | `PASS` |
| `/api/v1/web-pages/{id}` | GET | `WebPage` | `PASS` |
| `/api/v1/web-pages/{id}/versions` | GET | `WebPageVersion` | `PASS` |
