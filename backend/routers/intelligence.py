from fastapi import APIRouter
from tracenest import logger
from intelligence.comparison import ComparisonEngine
from intelligence.reporting import ReportGenerator

router = APIRouter(prefix="/api/v1/intelligence", tags=["Civic Intelligence"])

@router.get("/compare/representatives")
def compare_reps(rep_a: str, rep_b: str):
    logger.info("GET /api/v1/intelligence/compare/representatives – Comparing representatives", rep_a=rep_a, rep_b=rep_b)
    logger.debug("Delegating to ComparisonEngine.compare_representatives", rep_a=rep_a, rep_b=rep_b)
    try:
        result = ComparisonEngine.compare_representatives(rep_a, rep_b)
        logger.info("Representative comparison completed", rep_a=rep_a, rep_b=rep_b)
        return result
    except Exception as e:
        logger.error("Representative comparison FAILED", rep_a=rep_a, rep_b=rep_b, error=str(e))
        raise

@router.post("/reports")
def create_report(report_type: str, scope: str):
    logger.info("POST /api/v1/intelligence/reports – Generating civic report", report_type=report_type, scope=scope)
    logger.debug("Delegating to ReportGenerator.generate_report", report_type=report_type, scope=scope)
    try:
        result = ReportGenerator.generate_report(report_type, scope, {})
        logger.info("Report generated successfully", report_type=report_type, scope=scope)
        return result
    except Exception as e:
        logger.error("Report generation FAILED", report_type=report_type, scope=scope, error=str(e))
        raise
