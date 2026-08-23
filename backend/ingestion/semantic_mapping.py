import re
from typing import Dict, Any, List

class SemanticMappingEngine:
    """
    Applies regex heuristics to infer semantic civic data types from raw dataset headers.
    """
    
    PATTERNS = {
        "DISTRICT": r"^(dist(_| )?name|district|dt_name|dtcode|dt_code)$",
        "STATE": r"^(state(_| )?name|st_name|stcode|state)$",
        "PERSON": r"^(name|full_name|candidate_name|member_name|beneficiary_name)$",
        "FINANCIAL_YEAR": r"^(fy|fin_year|financial(_| )?year|year)$",
        "AMOUNT": r"^(amount|total|expenditure|cost|fund|budget|allocation)(_in_rs)?$",
        "DATE": r"^(date|dt|created_at|updated_at|dob|date_of_birth)$",
        "GENDER": r"^(sex|gender)$",
        "PARTY": r"^(party|party_name)$",
        "AGE": r"^(age)$",
        "VILLAGE": r"^(village|vill|vill_name|gp_name|gram_panchayat)$",
        "WARD": r"^(ward|ward_no|ward_name)$"
    }
    
    def map_schema(self, schema: Dict[str, Any]) -> List[Dict[str, Any]]:
        mapped_fields = []
        for col in schema.get("columns", []):
            name = str(col["name"]).strip().lower()
            semantic_type = "UNKNOWN"
            confidence = 0.0
            
            for sem_type, pattern in self.PATTERNS.items():
                if re.search(pattern, name):
                    semantic_type = sem_type
                    confidence = 0.95
                    break
                    
            if semantic_type == "UNKNOWN":
                # Fallback heuristics
                if "id" in name or "code" in name:
                    semantic_type = "IDENTIFIER"
                    confidence = 0.6
                elif col.get("type") == "DATETIME":
                    semantic_type = "DATE"
                    confidence = 0.8
                    
            mapped_fields.append({
                "original_name": col["name"],
                "semantic_type": semantic_type,
                "confidence": confidence,
                "status": "MAPPED" if confidence >= 0.8 else "NEEDS_REVIEW"
            })
            
        return mapped_fields
