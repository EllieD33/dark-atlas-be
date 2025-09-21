import sys
from pathlib import Path

backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

import asyncio
import json
from aiohttp import ClientSession
from sqlalchemy.exc import SQLAlchemyError
from app.db import AsyncSessionLocal
from app.logger import get_logger
from app.ingestion.abuseipdb_client import fetch_aipdb_blacklist
from app.services.ioc_application_service import store_abuseipdb_data

logger = get_logger(__name__)

DATA_CACHE_FILE = (backend_dir / "data" / "abuseipdb_blacklist.json").resolve()

async def fetch_and_cache_abuseipdb(http_session: ClientSession) -> dict:
    """Fetch the full AbuseIPDB blacklist and save to local JSON cache."""
    DATA_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    if DATA_CACHE_FILE.exists():
        logger.info("Cache exists, skipping API fetch")
        with DATA_CACHE_FILE.open("r") as f:
            return json.load(f)

    data = await fetch_aipdb_blacklist(http_session)

    if not data or "data" not in data:
        logger.warning("No data fetched from AbuseIPDB.")
        return {}

    with DATA_CACHE_FILE.open("w") as f:
        json.dump(data, f, indent=2)

    logger.info(f"Fetched and cached {len(data['data'])} IOCs from AbuseIPDB.")
    return data


async def seed_db_from_cache():
    """Load cached AbuseIPDB data and insert into the DB (idempotent)."""
    if not DATA_CACHE_FILE.exists():
        logger.error("Cache file not found. Run fetch_and_cache_abuseipdb first.")
        return

    with open(DATA_CACHE_FILE, "r") as f:
        cached_data = json.load(f)

    async with AsyncSessionLocal() as db_session:
        try:
            await store_abuseipdb_data(db_session, cached_data["data"])
            logger.info(f"Inserted {len(cached_data['data'])} IOCs into the DB (duplicates skipped).")
            logger.info("AbuseIPDB seed finished")
        except SQLAlchemyError:
            logger.exception("Error committing IOCs to the DB")
            logger.error("AbuseIPDB seed failed")



if __name__ == "__main__":
    async def main():
        async with ClientSession() as http_session:
            await fetch_and_cache_abuseipdb(http_session)
        await seed_db_from_cache()


    asyncio.run(main())
