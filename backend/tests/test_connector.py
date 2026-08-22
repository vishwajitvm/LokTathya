import pytest
import uuid
from ingestion.connector_factory import UniversalConnector
from models.source import Source, SourceEndpoint
from sqlalchemy.orm import Session
from core.database import SessionLocal

@pytest.fixture(scope="module")
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.mark.anyio
async def test_universal_connector_html_ingestion(db_session: Session):
    source = Source(name="Universal Connector Source", status="ACTIVE")
    db_session.add(source)
    db_session.commit()

    endpoint = SourceEndpoint(
        source_id=source.id,
        url="https://completion.gov.in/index.html",
        method="GET",
        enabled=True,
        status="ACTIVE"
    )
    db_session.add(endpoint)
    db_session.commit()

    connector = UniversalConnector(db_session)
    run_id = uuid.uuid4()
    
    mock_res = {
        "status": "SUCCESS",
        "status_code": 200,
        "content": b"<html><body><h1>Budget 2026</h1><table><tr><td>Data</td></tr></table></body></html>",
        "headers": {"content-type": "text/html"}
    }
    
    from unittest.mock import patch
    with patch("core.http_client.ResilientHTTPClient.fetch", return_value=mock_res):
        res = await connector.ingest_endpoint(endpoint.id, run_id)
        assert res["status"] == "SUCCESS"
        assert res["detected_format"] == "HTML"
        assert res["observations_count"] >= 1
