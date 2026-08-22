from core.database import SessionLocal
from entity_resolution.engine import EntityResolutionEngine as RealResolutionEngine
import uuid

class EntityResolutionEngine:
    def resolve(self, raw_value: str, target_table: str):
        db = SessionLocal()
        try:
            # Create a mock/default source ID if none is active
            source_id = uuid.uuid4()
            real_engine = RealResolutionEngine(db)
            res = real_engine.resolve_entity(raw_value, target_table, source_id)
            return {
                "raw_value": raw_value,
                "target_table": target_table,
                "confidence": res["confidence"],
                "status": res["status"],
                "method": res["method"]
            }
        finally:
            db.close()
