from fastapi import FastAPI
from app.api.v1 import iocs

app = FastAPI(title="DarkAtlas API")

app.include_router(iocs.router, prefix="/iocs", tags=["iocs"])

@app.get("/")
def root():
    return {"message": "DarkAtlas API is running"}
