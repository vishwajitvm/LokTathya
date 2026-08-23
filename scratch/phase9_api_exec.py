import requests
import json
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import uuid

CSV_CONTENT = """dist_name,population,budget_amount,fy,status
LUCKNOW,4589838,500000.00,2024-25,ACTIVE
KANPUR,4167999,400000.00,2024-25,ACTIVE
"""

class MockGovHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/csv')
        self.end_headers()
        self.wfile.write(CSV_CONTENT.encode('utf-8'))
        
    def log_message(self, format, *args):
        pass # Suppress logs

def run_server():
    server = HTTPServer(('0.0.0.0', 8085), MockGovHandler)
    server.serve_forever()

BASE_URL = "http://localhost:8001"

def run_tests():
    print("=== Phase 9 Execution Evidence ===")
    
    # Start mock server
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    time.sleep(1)
    
    # 1. Create Source
    print("\n1. Creating Source")
    source_payload = {
        "name": "Phase 9 Dataset Verification",
        "official_domain": "mock.gov.in",
        "authority_level": "STATE",
        "category": "TESTING"
    }
    r = requests.post(f"{BASE_URL}/api/v1/sources/", json=source_payload)
    source_id = r.json()["id"]
    
    # 2. Create Endpoint
    # Since docker accesses host as host.docker.internal
    print("\n2. Creating Endpoint")
    url = "http://host.docker.internal:8085/budget.csv"
    endpoint_payload = {
        "url": url,
        "method": "GET"
    }
    r = requests.post(f"{BASE_URL}/api/v1/sources/{source_id}/endpoints", json=endpoint_payload)
    ep_id = r.json()["endpoint_id"]
    
    # 3. Trigger Discovery -> fetch -> parse -> dataset schema
    print("\n3. Triggering Ingestion")
    # Forcing a direct fetch via Celery (using the API or a direct trigger script). 
    # Wait, discovery only pulls links. To pull this file, we should trigger fetch directly.
    # We can inject a fetch task using a script, or we can just trigger discovery and since it returns CSV, it will just download it.
    r = requests.post(f"{BASE_URL}/api/v1/discovery/runs?source_id={source_id}&max_pages=1")
    
    print("\nWaiting for pipeline (discovery -> fetch -> parse -> semantic mapping)...")
    time.sleep(6)
    
    # 4. Check Dataset Catalog
    print("\n4. Fetching Dataset Identity")
    r = requests.get(f"{BASE_URL}/api/v1/datasets?source_id={source_id}")
    datasets = r.json()
    print("Datasets:", json.dumps(datasets, indent=2))
    
    if datasets:
        ds_id = datasets[0]["id"]
        
        # 5. Check Versions
        print("\n5. Fetching Dataset Versions")
        r = requests.get(f"{BASE_URL}/api/v1/datasets/{ds_id}/versions")
        versions = r.json()
        print("Versions:", json.dumps(versions, indent=2))
        
        # 6. Check Schema
        print("\n6. Fetching Dataset Schema & Semantic Mappings")
        r = requests.get(f"{BASE_URL}/api/v1/datasets/{ds_id}/schema")
        print("Schema:", json.dumps(r.json(), indent=2))
        
        # 7. Check Quality Profile
        print("\n7. Fetching Dataset Quality Profile")
        r = requests.get(f"{BASE_URL}/api/v1/datasets/{ds_id}/quality")
        print("Quality:", json.dumps(r.json(), indent=2))
    else:
        print("Dataset was not created. Pipeline failed.")

if __name__ == "__main__":
    run_tests()
