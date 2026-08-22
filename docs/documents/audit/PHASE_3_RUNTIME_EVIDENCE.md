# Phase 3 Runtime Evidence Report

This document records the runtime evidence observed during the final completion gate execution.

---

## 1. Docker Compose Services Status
The complete service stack has been rebuilt and restarted. All 7 containers are fully active and healthy:

```
NAME                  IMAGE                                      STATUS
loktathya_backend     loktathya-backend                          Up (healthy)
loktathya_frontend    loktathya-frontend                         Up (healthy)
loktathya_minio       minio/minio:RELEASE.2024-05-10T01-41-38Z   Up (healthy)
loktathya_postgres    loktathya-postgres                         Up (healthy)
loktathya_redis       redis:7-alpine                             Up (healthy)
loktathya_scheduler   loktathya-scheduler                        Up (healthy)
loktathya_worker      loktathya-worker                           Up (healthy)
```

---

## 2. Database Migration Head
The Alembic head has been fully upgraded to:
`f1c2c1d84e03_p3_registry_endpoint_expansion`

Executing `alembic current` inside the backend container displays:
`f1c2c1d84e03 (head)`

---

## 3. Test Suite Count and Results
The test suite contains 43 tests (including the new integration and security hardening test suites). All 43 tests pass cleanly inside the backend container:

```
collected 43 items

tests/test_api_extensions.py ....                                        [  9%]
tests/test_celery_routes.py .                                            [ 11%]
tests/test_completion_gate.py ....                                       [ 20%]
tests/test_discovery.py ..                                               [ 25%]
tests/test_end_to_end_vertical.py ..                                     [ 30%]
tests/test_format_detector.py ....                                       [ 39%]
tests/test_http_client.py ....                                           [ 48%]
tests/test_infra.py .                                                    [ 51%]
tests/test_link_extractor.py ...                                         [ 58%]
tests/test_parsers.py ........                                           [ 76%]
tests/test_security_hardening.py ...                                     [ 83%]
tests/test_storage.py .                                                  [ 86%]
tests/test_url_utils.py ....                                             [ 95%]
tests/test_versioning.py ..                                              [100%]

======================== 43 passed in 9.13s ========================
```

---

## 4. Redis and Celery Task Queues
Celery routes tasks dynamically based on queue configurations:
- `source_discovery`
- `fetch`
- `html`
- `pdf`
- `ocr`
- `tabular`
- `gis`
- `normalization`
- `entity_resolution`
- `reconciliation`

Redis broker connection matches:
`redis://redis:6379/0`
All workers successfully bind to Redis on startup and wait for queue notifications.
