from fastapi import APIRouter
from intelligence.comparison import ComparisonEngine
from intelligence.reporting import ReportGenerator

router = APIRouter(prefix="/api/v1/intelligence", tags=["Civic Intelligence"])

@router.get("/compare/representatives")
def compare_reps(rep_a: str, rep_b: str):
    return ComparisonEngine.compare_representatives(rep_a, rep_b)

@router.post("/reports")
def create_report(report_type: str, scope: str):
    return ReportGenerator.generate_report(report_type, scope, {})
