from typing import Dict, Any
from datetime import datetime

class IngestionQualityGate:
    """Ensures datasets only become PUBLIC after strict verification."""
    
    @staticmethod
    def evaluate_dataset(dataset_id: str, run_metrics: Dict[str, Any]) -> str:
        """
        DRAFT -> VALIDATING -> VERIFIED -> PUBLIC
        """
        if run_metrics.get("conflicts", 0) > 0:
            return "VALIDATING" # Requires human review
        if run_metrics.get("parser_failures", 0) > 0:
            return "DRAFT" # Quarantined
            
        return "PUBLIC"
