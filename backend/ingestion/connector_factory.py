import uuid
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from models.source import Source, SourceEndpoint, FetchEvent, Document, ContentVersion
from models.observation import Observation
from core.format_detector import FormatDetector
from ingestion.parser_factory import ParserFactory
from storage.minio_client import MinIOStorageService
from core.http_client import ResilientHTTPClient
from tracenest import logger

class UniversalConnector:
    """
    Step 4: Universal Connector Contract.
    Implements a standardized ingestion lifecycle: discover, fetch, parse, normalize, emit.
    """

    def __init__(self, db_session: Session):
        self.db = db_session
        self.storage = MinIOStorageService()

    async def ingest_endpoint(self, endpoint_id: uuid.UUID, run_id: uuid.UUID) -> Dict[str, Any]:
        """
        Standardized lifecycle execution for a single endpoint.
        """
        endpoint = self.db.query(SourceEndpoint).filter(SourceEndpoint.id == endpoint_id).first()
        if not endpoint:
            return {"status": "ERROR", "message": "Endpoint not found"}

        logger.info("Executing Universal Connector fetch", endpoint_id=str(endpoint_id), url=endpoint.url)

        # 1. FETCH STAGE
        client = ResilientHTTPClient()
        try:
            res = await client.fetch(
                url=endpoint.url, 
                rate_limit_rpm=endpoint.rate_limit_rpm
            )
            if res["status"] != "SUCCESS":
                return {"status": "FAILED", "stage": "FETCH", "error": res.get("error")}
            
            content_bytes = res["content"]
            content_type = res["headers"].get("content-type", "")
            
        finally:
            await client.close()

        # 2. RAW STORAGE STAGE
        content_hash = hashlib.sha256(content_bytes).hexdigest()
        storage_path = f"sources/{endpoint.source_id}/endpoints/{endpoint.id}/versions/{content_hash}/raw"
        self.storage.put(storage_path, content_bytes, content_type)

        # 3. DETECT FORMAT
        detection = FormatDetector.detect_format(content_bytes, content_type, endpoint.url)
        detected_format = detection["detected_format"]

        # 4. PARSE & NORMALIZE STAGE
        meta = {
            "document_id": str(endpoint_id),
            "source_id": str(endpoint.source_id),
            "storage_path": storage_path,
            "base_url": endpoint.url,
            "detected_format": detected_format
        }
        
        try:
            parser = ParserFactory.get_parser(detected_format)
            parsed_res = parser.parse(content_bytes, meta)
            
            if parsed_res["status"] != "SUCCESS":
                return {"status": "FAILED", "stage": "PARSE", "error": parsed_res.get("status")}
                
        except Exception as e:
            logger.error("Parser crash", endpoint_id=str(endpoint_id), error=str(e))
            return {"status": "FAILED", "stage": "PARSE", "error": str(e)}

        # 5. EMIT OBSERVATIONS
        observations_created = []
        structured = parsed_res["structured_content"]
        
        # If it is HTML, extract structured tables and emit observations
        if detected_format == "HTML" and "tables" in structured:
            for idx, table in enumerate(structured["tables"]):
                obs = Observation(
                    source_id=endpoint.source_id,
                    entity_type="html_table",
                    field_name=table.get("caption") or f"table_{idx}",
                    raw_value=str(table.get("rows")),
                    normalized_value=table,
                    status="VALIDATED",
                    observed_at=datetime.now(timezone.utc)
                )
                self.db.add(obs)
                observations_created.append(obs)
                
        # Emit general document observations for parsing success
        doc_obs = Observation(
            source_id=endpoint.source_id,
            entity_type="document_metadata",
            field_name="parse_summary",
            raw_value=parsed_res["text_content"][:1000],
            normalized_value={"parser": parsed_res["parser_name"], "format": detected_format},
            status="VALIDATED",
            observed_at=datetime.now(timezone.utc)
        )
        self.db.add(doc_obs)
        observations_created.append(doc_obs)
        
        self.db.commit()

        return {
            "status": "SUCCESS",
            "detected_format": detected_format,
            "storage_path": storage_path,
            "observations_count": len(observations_created)
        }
