from typing import Dict, Any, List

class ReconciliationEngine:
    """Deterministic logic for handling multiple official observations."""
    
    @staticmethod
    def evaluate_observations(obs_a: Dict[str, Any], obs_b: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate two observations of the same logical entity field.
        Returns the conflict status.
        """
        # If dates are strictly different and one explicitly supersedes
        if obs_a.get("published_at") != obs_b.get("published_at"):
            # Mock logic: assuming B is newer
            return {"status": "SUPERSEDED", "canonical": obs_b, "history": [obs_a]}
            
        if obs_a.get("normalized_value") == obs_b.get("normalized_value"):
            return {"status": "CONSISTENT", "canonical": obs_a}
            
        # If values differ and dates are the same (or unknown)
        return {
            "status": "CONFLICTING",
            "canonical": None,
            "requires_review": True,
            "observations": [obs_a, obs_b]
        }
