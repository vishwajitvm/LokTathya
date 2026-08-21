from typing import Dict, Any, List
from .tools import CivicTools

class QueryPlanner:
    def plan(self, query: str) -> List[str]:
        # Dummy routing logic based on keywords
        if "spent" in query.lower() or "budget" in query.lower():
            return ["get_financial_summary", "search_documents"]
        elif "district" in query.lower():
            return ["get_geography"]
        return ["search_documents"]

    def execute(self, plan: List[str], query: str) -> Dict[str, Any]:
        evidence = {}
        for tool in plan:
            if tool == "get_financial_summary":
                evidence["finance"] = CivicTools.get_financial_summary("proj-1")
            elif tool == "search_documents":
                evidence["docs"] = CivicTools.search_documents(query, {})
        return evidence
