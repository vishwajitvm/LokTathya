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
        self.storage.put(storage_path, content_bytes, res["headers"].get("content-type", "") if isinstance(res.get("headers"), dict) else "")

        # 3. IDENTIFY FORMAT
        content_type = res["headers"].get("Content-Type", "") if isinstance(res.get("headers"), dict) else ""
        format_info = FormatDetector.detect_format(content_bytes, content_type, endpoint.url)
        detected_format = format_info["detected_format"]

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

        # PHASE 9: DATASET INTELLIGENCE LAYER
        observations_created = []
        dataset_created = False
        
        if detected_format in ["CSV", "XLSX", "TSV", "JSON"]:
            from models.dataset import Dataset, DatasetVersion, DatasetSchema, DatasetQualityProfile, DatasetField
            from ingestion.schema_inference import SchemaInferenceEngine
            from ingestion.semantic_mapping import SemanticMappingEngine
            import uuid
            
            # Create or update dataset identity based on endpoint
            # A true production system might use LLM to decide if it's a new dataset or an existing one
            # For now, 1 Endpoint = 1 Dataset Identity
            ds = self.db.query(Dataset).filter(Dataset.name == endpoint.url).first()
            if not ds:
                ds = Dataset(
                    source_id=endpoint.source_id,
                    name=endpoint.url,
                    description=f"Auto-generated dataset from {detected_format}"
                )
                self.db.add(ds)
                self.db.flush()
                
            # Create DatasetVersion
            d_version = DatasetVersion(
                dataset_id=ds.id,
                source_endpoint_id=endpoint.id,
                content_hash=content_hash,
                valid_from=datetime.now(timezone.utc),
                change_classification="NEW"
            )
            self.db.add(d_version)
            self.db.flush()
            
            # Infer Schema & Quality Profile
            inf_engine = SchemaInferenceEngine(sample_rows=1000)
            inferred_schema, quality_profile = inf_engine.infer_schema(content_bytes, detected_format)
            
            d_schema = DatasetSchema(
                dataset_version_id=d_version.id,
                inferred_schema=inferred_schema
            )
            self.db.add(d_schema)
            
            d_quality = DatasetQualityProfile(
                dataset_version_id=d_version.id,
                row_count=quality_profile["row_count"],
                column_count=quality_profile["column_count"],
                null_ratio=quality_profile["null_ratio"],
                duplicate_row_ratio=quality_profile["duplicate_row_ratio"]
            )
            self.db.add(d_quality)
            self.db.flush()
            
            # Semantic Mapping
            map_engine = SemanticMappingEngine()
            mapped_fields = map_engine.map_schema(inferred_schema)
            for m in mapped_fields:
                d_field = DatasetField(
                    dataset_schema_id=d_schema.id,
                    original_name=m["original_name"],
                    semantic_type=m["semantic_type"],
                    confidence=m["confidence"],
                    status=m["status"]
                )
                self.db.add(d_field)
                
            dataset_created = True

        # 5. EMIT OBSERVATIONS
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
