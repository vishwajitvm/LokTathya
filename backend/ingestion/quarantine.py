import uuid
from datetime import datetime

class QuarantineManager:
    @staticmethod
    def quarantine_record(source_id: str, version_id: str, stage: str, error: str, raw_data: dict):
        # In real code this writes to the DB table prov_quarantine (or similar)
        return {
            "quarantine_id": str(uuid.uuid4()),
            "source_id": source_id,
            "version_id": version_id,
            "stage": stage,
            "error": error,
            "timestamp": datetime.utcnow().isoformat()
        }
