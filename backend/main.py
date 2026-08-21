from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uuid
import time
import logging
from routers import sources, analytics, search, geography, chat, data_quality, elections, representatives, coverage, ingestion, intelligence, geographies_history

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TraceNest")

app = FastAPI(title="LokTathya API", version="1.0.0", openapi_url="/api/v1/openapi.json")

@app.get('/health')
def health():
    return {'status': 'healthy'}

@app.middleware("http")
async def add_request_id_and_trace(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.time()
    request.state.request_id = request_id
    logger.info(f"[TraceNest] START req_id={request_id} path={request.url.path}")
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(process_time)
        logger.info(f"[TraceNest] END req_id={request_id} status={response.status_code} time={process_time:.4f}s")
        return response
    except Exception as exc:
        logger.error(f"[TraceNest] ERROR req_id={request_id} err={str(exc)}")
        return JSONResponse(status_code=500, content={"code": "INTERNAL_ERROR", "request_id": request_id})

app.include_router(sources.router)
app.include_router(analytics.router)
app.include_router(search.router)
app.include_router(geography.router)
app.include_router(chat.router)
app.include_router(data_quality.router)
app.include_router(elections.router)
app.include_router(representatives.router)
app.include_router(coverage.router)
app.include_router(ingestion.router)
app.include_router(intelligence.router)
app.include_router(geographies_history.router)
