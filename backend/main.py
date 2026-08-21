from fastapi import FastAPI
from routers import sources

app = FastAPI(title="LokTathya API")
app.include_router(sources.router)

@app.get("/health")
def health():
    return {"status": "healthy"}
