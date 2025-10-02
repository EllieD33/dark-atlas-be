import sys
import json
import asyncio
from pathlib import Path
from aiohttp import ClientSession
from sqlalchemy.exc import SQLAlchemyError

from app.db import AsyncSessionLocal
from app.logger import get_logger
from app.services.ioc_application_service import store_urlhaus_data
from app.ingestion.utils import fetch_json

logger = get_logger(__name__)

backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

DATA_CACHE_FILE = (backend_dir / "data" / "urlhaus_recent.json").resolve()


async def fetch_and_cache_urlhaus_recent(http_session: ClientSession) -> dict:
    """Fetch the recent UrlHaus list and save to local JSON cache."""
    DATA_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)

    if DATA_CACHE_FILE.exists():
        logger.info("Cache exists, loading from disk")
        with DATA_CACHE_FILE.open("r") as f:
            return json.load(f)

    logger.info("Fetching UrlHaus recent feed")
    data = await fetch_json(
        session=http_session,
        url="https://urlhaus.abuse.ch/downloads/json_recent/"
    )

    if not data:
        logger.warning("No data fetched from UrlHaus.")
        return {}

    with DATA_CACHE_FILE.open("w") as f:
        json.dump(data, f, indent=2)

    logger.info(f"Fetched and cached {len(data.get('data', []))} entries from UrlHaus.")
    return data


async def seed_db_from_cache():
    """Load cached UrlHaus data and insert into the DB (idempotent)."""
    if not DATA_CACHE_FILE.exists():
        logger.error("Cache file not found. Run fetch_and_cache_urlhaus_recent first.")
        return

    with DATA_CACHE_FILE.open("r") as f:
        cached_data = json.load(f)

    total_reports = sum(len(reports) for reports in cached_data.values())
    logger.info(f"Attempting to insert {total_reports} UrlHaus reports (duplicates may be skipped).")

    async with AsyncSessionLocal() as db_session:
        try:
            entries = [(entry_id, reports) for entry_id, reports in cached_data.items()]
            await store_urlhaus_data(db_session, entries)
            logger.info("UrlHaus seed finished")
        except SQLAlchemyError:
            logger.exception("Error committing IOCs to the DB")
            logger.error("UrlHaus seed failed")


if __name__ == "__main__":
    async def main():
        async with ClientSession() as http_session:
            await fetch_and_cache_urlhaus_recent(http_session)
        await seed_db_from_cache()

    asyncio.run(main())
