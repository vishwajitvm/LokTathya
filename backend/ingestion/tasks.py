import uuid
import asyncio
from datetime import datetime, timezone
from core.celery_app import celery_app
from core.database import SessionLocal
from ingestion.connector_factory import UniversalConnector
from services.scheduler import SourceScheduler
from ingestion.discovery import ControlledDiscoveryEngine
from models.source import Source, SourceEndpoint
from tracenest import logger

@celery_app.task(name='ingestion.tasks.poll_scheduler')
def poll_scheduler():
    logger.info("Executing periodic poll_scheduler task")
    db = SessionLocal()
    try:
        now = datetime.now(timezone.utc)
        due_endpoints = db.query(SourceEndpoint).filter(
            SourceEndpoint.enabled == True,
            SourceEndpoint.status != "DISABLED",
            (SourceEndpoint.next_scheduled_at == None) | (SourceEndpoint.next_scheduled_at <= now)
        ).all()
        
        triggered_count = 0
        for ep in due_endpoints:
            run_id = uuid.uuid4()
            # Dispatch celery fetch task asynchronously
            fetch_task.delay(str(ep.id), str(run_id))
            
            # Update scheduled time to prevent duplicate triggering
            ep.next_scheduled_at = SourceScheduler.calculate_next_run(ep.refresh_frequency or "DAILY", now)
            ep.last_checked = now
            triggered_count += 1
            
        db.commit()
        return {"status": "SUCCESS", "triggered_count": triggered_count}
    except Exception as e:
        logger.error("Poll scheduler task failed", error=str(e))
        return {"status": "FAILED", "error": str(e)}
    finally:
        db.close()


@celery_app.task(name='ingestion.tasks.source_discovery')
def source_discovery(source_id_str: str):
    logger.info("Executing Celery source_discovery task", source_id=source_id_str)
    db = SessionLocal()
    try:
        source_id = uuid.UUID(source_id_str)
        source = db.query(Source).filter(Source.id == source_id).first()
        if not source:
            return {"status": "ERROR", "message": "Source not found"}

        # Perform discovery on the official domain
        if source.official_domain:
            engine = ControlledDiscoveryEngine(allowed_domains={source.official_domain})
            # Try to discover sitemap or raw html links
            sitemap_url = f"https://{source.official_domain}/sitemap.xml"
            discovered_urls = asyncio.run(engine.discover_sitemap(sitemap_url))
            
            # Register discovered URLs as endpoints
            for url in discovered_urls:
                existing = db.query(SourceEndpoint).filter(SourceEndpoint.url == url).first()
                if not existing:
                    new_ep = SourceEndpoint(
                        source_id=source.id,
                        url=url,
                        method="GET",
                        status="ACTIVE",
                        enabled=True
                    )
                    db.add(new_ep)
            db.commit()
            return {"status": "SUCCESS", "discovered_count": len(discovered_urls)}
        return {"status": "SUCCESS", "message": "No domain configured"}
    except Exception as e:
        logger.error("Source discovery task failed", error=str(e))
        return {"status": "FAILED", "error": str(e)}
    finally:
        db.close()

@celery_app.task(name='ingestion.tasks.fetch_task')
def fetch_task(endpoint_id_str: str, run_id_str: str):
    logger.info("Executing Celery fetch_task", endpoint_id=endpoint_id_str)
    db = SessionLocal()
    try:
        endpoint_id = uuid.UUID(endpoint_id_str)
        run_id = uuid.UUID(run_id_str)
        
        connector = UniversalConnector(db)
        res = asyncio.run(connector.ingest_endpoint(endpoint_id, run_id))
        
        if res["status"] == "SUCCESS":
            SourceScheduler.handle_fetch_success(db, endpoint_id)
        else:
            SourceScheduler.handle_fetch_failure(db, endpoint_id, res.get("error", "Unknown"))
            
        return res
    except Exception as e:
        logger.error("Fetch task failed", error=str(e))
        return {"status": "FAILED", "error": str(e)}
    finally:
        db.close()

@celery_app.task(name='ingestion.tasks.parse_html')
def parse_html(content_path: str):
    return {"status": "SUCCESS", "parser": "HTML"}

@celery_app.task(name='ingestion.tasks.parse_pdf')
def parse_pdf(content_path: str):
    return {"status": "SUCCESS", "parser": "PDF"}

@celery_app.task(name='ingestion.tasks.ocr_task')
def ocr_task(content_path: str):
    return {"status": "SUCCESS", "parser": "OCR"}

@celery_app.task(name='ingestion.tasks.parse_tabular')
def parse_tabular(content_path: str):
    return {"status": "SUCCESS", "parser": "TABULAR"}

@celery_app.task(name='ingestion.tasks.parse_gis')
def parse_gis(content_path: str):
    return {"status": "SUCCESS", "parser": "GIS"}

@celery_app.task(name='ingestion.tasks.normalize')
def normalize(data: dict):
    return {"status": "SUCCESS"}

@celery_app.task(name='ingestion.tasks.resolve_entities')
def resolve_entities(data: dict):
    return {"status": "SUCCESS"}

@celery_app.task(name='ingestion.tasks.reconcile')
def reconcile(data: dict):
    return {"status": "SUCCESS"}
