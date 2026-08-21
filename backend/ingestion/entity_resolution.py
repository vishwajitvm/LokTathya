class EntityResolutionEngine:
    def resolve(self, raw_value: str, target_table: str):
        # Cache-free Postgres lookup mock
        confidence = 0.0
        status = "UNRESOLVED"
        
        if raw_value == "Ministry of Finance":
            confidence = 1.0
            status = "AUTO_ACCEPTED"
        elif "Ministry" in raw_value:
            confidence = 0.5
            status = "HUMAN_REVIEW"

        return {
            "raw_value": raw_value,
            "target_table": target_table,
            "confidence": confidence,
            "status": status,
            "method": "exact_match_fallback_fuzzy"
        }
