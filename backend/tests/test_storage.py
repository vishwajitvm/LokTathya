import pytest
from storage.minio_client import MinIOStorageService

def test_minio_roundtrip():
    service = MinIOStorageService()
    
    test_key = "tests/test_object.txt"
    test_data = b"Hello, LokTathya Raw Storage!"
    test_metadata = {"source_id": "test-src", "version": "1"}
    
    # 1. Put
    assert service.put(test_key, test_data, content_type="text/plain", metadata=test_metadata)
    
    # 2. Exists
    assert service.exists(test_key)
    
    # 3. Get
    retrieved = service.get(test_key)
    assert retrieved == test_data
    
    # 4. Metadata
    meta = service.get_metadata(test_key)
    assert meta is not None
    assert meta["content_type"] == "text/plain"
    assert meta["size"] == len(test_data)
    # Boto3 lowercases metadata keys
    assert meta["metadata"]["source_id"] == "test-src"
    assert meta["metadata"]["version"] == "1"
    
    # 5. Delete
    assert service.delete_if_allowed(test_key)
    assert not service.exists(test_key)
