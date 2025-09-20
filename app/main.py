from fastapi import FastAPI
from app.api.v1 import iocs

app = FastAPI(
    title="DarkAtlas Threat API",
    version="0.1.0",
    description="API for ingesting and querying threat intelligence indicators (IOCs)."
)

app.include_router(iocs.router, prefix="/iocs", tags=["IOCs"])

@app.get("/", tags=["root"])
async def root():
    """
    API root endpoint.
    Provides metadata and links to documentation.
    """
    return {
        "service": "DarkAtlas Threat API",
        "version": "0.1.0",
        "docs_url": "/docs"
    }
