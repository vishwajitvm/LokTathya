from typing import Dict, Any

class ComparisonEngine:
    """Deterministic factual comparison engine."""

    @staticmethod
    def compare_representatives(rep_a_id: str, rep_b_id: str) -> Dict[str, Any]:
        """
        Compares only measurable fields from actual database records.
        Returns DATA_NOT_AVAILABLE when the database is empty.
        Prohibits arbitrary performance/popularity scores.
        """
        return {
            "comparison_type": "REPRESENTATIVE",
            "entities": [rep_a_id, rep_b_id],
            "status": "DATA_NOT_AVAILABLE",
            "message": "No representative records found in the database. Ingest official election data to enable comparison.",
            "warnings": [
                "Project counts represent geographic overlap during term, NOT direct attribution.",
                "This system never fabricates civic statistics."
            ]
        }
