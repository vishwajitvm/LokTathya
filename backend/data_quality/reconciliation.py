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
        pub_a = obs_a.get("published_at")
        pub_b = obs_b.get("published_at")
        if pub_a and pub_b and pub_a != pub_b:
            try:
                # Compare values; if string ISO timestamps, direct comparison works
                if str(pub_b) > str(pub_a):
                    return {"status": "SUPERSEDED", "canonical": obs_b, "history": [obs_a]}
                else:
                    return {"status": "SUPERSEDED", "canonical": obs_a, "history": [obs_b]}
            except Exception:
                pass
            
        if obs_a.get("normalized_value") == obs_b.get("normalized_value"):
            return {"status": "CONSISTENT", "canonical": obs_a}
            
        # If values differ and dates are the same (or unknown)
        return {
            "status": "CONFLICTING",
            "canonical": None,
            "requires_review": True,
            "observations": [obs_a, obs_b]
        }
