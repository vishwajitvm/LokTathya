# P2 Ingestion Failure Matrix

This matrix documents the isolation and recovery behavior of the processing pipeline when encountering common failures.

| Failure Mode | Detection | Handling Strategy | Target State |
| :--- | :--- | :--- | :--- |
| SSRF Attempt | DNS Resolver check | Block request immediately | `BLOCKED` |
| Malformed PDF | PyPDF stream read fail | Move to Quarantine; log error | `QUARANTINED` |
| Size Limit Exceeded | Content-Length check | Terminate connection early | `BLOCKED` |
| Connection Timeout | HTTP Client exception | Retry with exponential backoff | `FETCH_PENDING` |
| DB Collision | IntegrityError catch | Skip version generation | `NO_CHANGE` |

## Recovery Paths
Refer to [failure-recovery.mmd](file:///c:/python/LokTathya/docs/diagrams/11-failure-recovery/failure-recovery.mmd) for structural recovery workflows.
