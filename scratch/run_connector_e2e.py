import asyncio
import sys
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.source import Source, SourceEndpoint, IngestionRun
from ingestion.connector_factory import UniversalConnector
import uuid

async def run_e2e_ingestion():
    db: Session = SessionLocal()
    
    # 1. Create a Source
    src = Source(
        name="Mock Finance Department",
        official_domain="finance.mock.gov.in",
        authority_level="STATE",
        category="FINANCE"
    )
    db.add(src)
    db.commit()
    db.refresh(src)
    print(f"Created Source: {src.id}")
    
    # 2. Create Endpoint pointing to our local python mock server
    ep = SourceEndpoint(
        source_id=src.id,
        url="http://host.docker.internal:8085/budget.csv",
        method="GET",
        status="ACTIVE"
    )
    db.add(ep)
    db.commit()
    db.refresh(ep)
    print(f"Created Endpoint: {ep.id}")
    
    # 3. Trigger Universal Connector
    print(f"Triggering UniversalConnector for Endpoint {ep.id}...")
    run_id = uuid.uuid4()
    connector = UniversalConnector(db)
    result = await connector.ingest_endpoint(ep.id, run_id)
    print(f"Connector result: {result}")
    
    # 4. Read back Dataset and Profile from DB
    from models.dataset import Dataset, DatasetVersion, DatasetSchema, DatasetQualityProfile, DatasetField
    
    ds = db.query(Dataset).filter(Dataset.source_id == src.id).first()
    if ds:
        print(f"\n--- DATASET IDENTIFIED ---")
        print(f"Dataset ID: {ds.id}, Name: {ds.name}, Status: {ds.status}")
        
        dv = db.query(DatasetVersion).filter(DatasetVersion.dataset_id == ds.id).first()
        print(f"\n--- DATASET VERSION ---")
        print(f"Version ID: {dv.id}, Hash: {dv.content_hash}, Created: {dv.valid_from}")
        
        profile = db.query(DatasetQualityProfile).filter(DatasetQualityProfile.dataset_version_id == dv.id).first()
        print(f"\n--- QUALITY PROFILE ---")
        print(f"Rows: {profile.row_count}, Columns: {profile.column_count}")
        print(f"Null Ratio: {profile.null_ratio}, Duplicates: {profile.duplicate_row_ratio}")
        
        schema = db.query(DatasetSchema).filter(DatasetSchema.dataset_version_id == dv.id).first()
        print(f"\n--- INFERRED SCHEMA ---")
        print(schema.inferred_schema)
        
        fields = db.query(DatasetField).filter(DatasetField.dataset_schema_id == schema.id).all()
        print(f"\n--- SEMANTIC MAPPING ---")
        for f in fields:
            print(f"Column: {f.original_name:<15} | Type: {f.semantic_type:<15} | Confidence: {f.confidence:<5} | Status: {f.status}")
            
    else:
        print("\nFAIL: Dataset was not created by the connector.")
    
if __name__ == "__main__":
    asyncio.run(run_e2e_ingestion())
