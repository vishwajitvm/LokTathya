from typing import Dict, Optional

class ElectionAnalytics:
    """Deterministic logic for historical election metrics."""
    
    @staticmethod
    def calculate_vote_share(candidate_votes: int, valid_votes: int) -> Dict[str, Optional[float]]:
        if not valid_votes or valid_votes == 0:
            return {"vote_share": None, "status": "INSUFFICIENT_DATA"}
        return {"vote_share": candidate_votes / valid_votes, "status": "COMPLETE"}

    @staticmethod
    def calculate_turnout(votes_polled: int, registered_electors: int) -> Dict[str, Optional[float]]:
        if not registered_electors or registered_electors == 0:
            return {"turnout": None, "status": "INSUFFICIENT_DATA"}
        return {"turnout": votes_polled / registered_electors, "status": "COMPLETE"}

    @staticmethod
    def calculate_winning_margin(winner_votes: int, runner_up_votes: int) -> Dict[str, Optional[int]]:
        if winner_votes is None or runner_up_votes is None:
            return {"margin": None, "status": "INSUFFICIENT_DATA"}
        return {"margin": winner_votes - runner_up_votes, "status": "COMPLETE"}
