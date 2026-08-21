from typing import Dict, Any, List

class CivicTools:
    """Strictly typed deterministic tools for the LLM. Prevents raw SQL generation."""
    
    @staticmethod
    def get_financial_summary(project_id: str) -> Dict[str, Any]:
        return {"allocated": 1000, "spent": 500, "utilization_rate": 0.5, "status": "COMPLETE"}
        
    @staticmethod
    def search_documents(query: str, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [{"text": "Budget summary chunk", "citation": {"source_name": "MoF", "page": 10}}]
        
    @staticmethod
    def get_geography(name: str, type: str) -> Dict[str, Any]:
        return {"id": "geo-123", "name": name, "type": type}
