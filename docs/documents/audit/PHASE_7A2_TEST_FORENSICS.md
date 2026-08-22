# Phase 7A-2 Test Forensics

This document records the classification of the test suite contributing to the 75 passed tests.

---

## 1. Test Suite Classification Matrix

| Test File | Category | Real DB? | Real Celery? | Real MinIO? | Real HTTP? | Real API? | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `test_access_policy.py` | SECURITY | No | No | No | Yes | No | PASS |
| `test_acquisition_api.py` | API / INTEGRATION | Yes | No | No | No | Yes | PASS |
| `test_api_extensions.py` | API | Yes | No | No | No | Yes | PASS |
| `test_canonicalizer.py` | DATA QUALITY | Yes | No | No | No | No | PASS |
| `test_celery_routes.py` | CELERY | No | No | No | No | No | PASS |
| `test_celery_tasks.py` | CELERY | Yes | No | Yes | No | No | PASS |
| `test_civic_apis.py` | API | Yes | No | Yes | No | Yes | PASS |
| `test_completion_gate.py` | INTEGRATION | Yes | No | No | No | No | PASS |
| `test_connector.py` | CONNECTOR | No | No | No | Yes | No | PASS |
| `test_discovery.py` | DISCOVERY | Yes | No | No | Yes | No | PASS |
| `test_end_to_end_vertical.py` | INTEGRATION | Yes | No | Yes | No | No | PASS |
| `test_entities_api.py` | API | Yes | No | No | No | Yes | PASS |
| `test_entity_resolution.py` | DATA QUALITY | Yes | No | No | No | No | PASS |
| `test_format_detector.py` | PARSER | No | No | No | No | No | PASS |
| `test_http_client.py` | HTTP | No | No | No | Yes | No | PASS |
| `test_infra.py` | INFRA | Yes | No | Yes | No | No | PASS |
| `test_large_file_safety.py` | SECURITY | No | No | No | No | No | PASS |
| `test_link_extractor.py` | PARSER | No | No | No | No | No | PASS |
| `test_normalization.py` | PARSER | No | No | No | No | No | PASS |
| `test_parsers.py` | PARSER | No | No | No | No | No | PASS |
| `test_scheduler.py` | CELERY | Yes | No | No | No | No | PASS |
| `test_scheduler_runtime.py` | CELERY | Yes | Yes | No | No | No | PASS |
| `test_security_hardening.py` | SECURITY | No | No | No | Yes | No | PASS |
| `test_storage.py` | STORAGE | No | No | Yes | No | No | PASS |
| `test_url_canonicalizer.py` | HTTP | No | No | No | No | N/A | PASS |
| `test_url_utils.py` | HTTP | No | No | No | No | N/A | PASS |
| `test_versioning.py` | INTEGRATION | Yes | No | Yes | No | No | PASS |
