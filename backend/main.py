from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# ── TraceNest SDK Integration ─────────────────────────────────────────
from tracenest import logger
from tracenest.fastapi.middleware import TraceNestMiddleware
from tracenest.ui.router import router as tracenest_ui_router
from tracenest.core.config import LOG_LEVELS

# Register TRACE level (Purple) – not in default config
LOG_LEVELS["TRACE"] = 5

# Patch Logger class to support logger.trace()
def _trace(self, message, **metadata):
    trace_id = metadata.pop("trace_id", None)
    from tracenest.logger import _log
    _log(level="TRACE", message=message, metadata=metadata, trace_id=trace_id)

logger.__class__.trace = _trace
# ── End TraceNest Patch ───────────────────────────────────────────────

from routers import (
    sources, analytics, search, geography, chat,
    data_quality, elections, representatives,
    coverage, ingestion, intelligence, geographies_history,
    web_pages, documents, discovery, quarantine
)

# ── App Initialization ───────────────────────────────────────────────
logger.info("Initializing LokTathya FastAPI Application", version="1.0.0")

app = FastAPI(
    title="LokTathya API",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
)

# ── TraceNest Middleware (auto-logs every HTTP request) ───────────────
app.add_middleware(TraceNestMiddleware)
logger.info("TraceNestMiddleware registered – all HTTP requests will be logged automatically")

# ── TraceNest UI (access at /tracenest) ──────────────────────────────
app.include_router(tracenest_ui_router)
logger.info("TraceNest UI mounted at /tracenest")

# ── Health Check ─────────────────────────────────────────────────────
@app.get('/health')
def health():
    logger.debug("Health check endpoint called")
    return {'status': 'healthy'}

# ── Startup / Shutdown Events ────────────────────────────────────────
@app.on_event("startup")
async def on_startup():
    logger.info("LokTathya API server STARTED – all systems operational")
    logger.info(
        "Registered routers",
        routers=[
            "sources", "analytics", "search", "geography", "chat",
            "data_quality", "elections", "representatives", "coverage",
            "ingestion", "intelligence", "geographies_history",
        ],
    )

@app.on_event("shutdown")
async def on_shutdown():
    logger.warning("LokTathya API server SHUTTING DOWN")

# ── Register All Routers ─────────────────────────────────────────────
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
app.include_router(web_pages.router)
app.include_router(documents.router)
app.include_router(discovery.router)
app.include_router(quarantine.router)

logger.info("All 16 API routers registered successfully")
