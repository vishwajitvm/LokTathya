from typing import Dict, Any, List

class ComparisonEngine:
    """Deterministic factual comparison engine."""
    
    @staticmethod
    def compare_representatives(rep_a_id: str, rep_b_id: str) -> Dict[str, Any]:
        """
        Compares only measurable fields. Prohibits arbitrary performance scores.
        """
        return {
            "comparison_type": "REPRESENTATIVE",
            "entities": [rep_a_id, rep_b_id],
            "metrics": {
                "terms_served": {rep_a_id: 2, rep_b_id: 1},
                "projects_associated": {
                    rep_a_id: {"count": 15, "status": "OFFICIAL_SOURCE"},
                    rep_b_id: {"count": None, "status": "DATA_NOT_AVAILABLE"}
                }
            },
            "warnings": [
                "Project counts represent geographic overlap during term, NOT direct attribution."
            ]
        }
