import requests
import json
import uuid
import time

BASE_URL = "http://localhost:8001"

def run_tests():
    print("=== Phase 8 Execution Evidence ===")
    
    # 1. System Health API
    print("\n1. Testing System Health API")
    r = requests.get(f"{BASE_URL}/api/v1/health/metrics")
    if r.status_code == 200:
        print("Success:", json.dumps(r.json(), indent=2))
    else:
        print("Error:", r.text)

    # 2. Create Source
    print("\n2. Creating Source with Taxonomy")
    source_payload = {
        "name": "Phase 8 Verification Source",
        "official_domain": "example.gov.in",
        "government_level": "UNION",
        "authority_level": "MINISTRY",
        "jurisdiction": "INDIA",
        "category": "TESTING"
    }
    r = requests.post(f"{BASE_URL}/api/v1/sources/", json=source_payload)
    if r.status_code == 201 or r.status_code == 200:
        source = r.json()
        source_id = source["id"]
        print("Success:", json.dumps(source, indent=2))
    else:
        print("Error:", r.text)
        return

    # 3. Create Endpoint with Rate Limit
    print("\n3. Creating Endpoint with Rate Limit")
    endpoint_payload = {
        "url": "https://example.gov.in/test-api",
        "method": "GET",
        "rate_limit_rpm": 30
    }
    r = requests.post(f"{BASE_URL}/api/v1/sources/{source_id}/endpoints", json=endpoint_payload)
    if r.status_code == 201 or r.status_code == 200:
        endpoint = r.json()
        print("Success:", json.dumps(endpoint, indent=2))
    else:
        print("Error:", r.text)

    # 4. Trigger Discovery
    print("\n4. Triggering Discovery (Deduplication Check)")
    r = requests.post(f"{BASE_URL}/api/v1/discovery/runs?source_id={source_id}&max_pages=5")
    if r.status_code == 200:
        print("Success:", json.dumps(r.json(), indent=2))
    else:
        print("Error:", r.text)
        
    print("\nWaiting for celery workers...")
    time.sleep(5)
    
    # 5. Fetch Candidates
    print("\n5. Checking Candidates")
    r = requests.get(f"{BASE_URL}/api/v1/discovery/candidates")
    if r.status_code == 200:
        print("Success:", json.dumps(r.json(), indent=2))
    else:
        print("Error:", r.text)
        
    # 6. Source History
    print("\n6. Checking Source History")
    r = requests.get(f"{BASE_URL}/api/v1/sources/{source_id}/history")
    if r.status_code == 200:
        print("Success:", json.dumps(r.json(), indent=2))
    else:
        print("Error:", r.text)

if __name__ == "__main__":
    run_tests()
