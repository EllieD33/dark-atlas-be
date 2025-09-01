from app.services.abuseipdb_service import transform_abuseipdb_entry
from app.repositories.ioc_repository import IOCRepository

async def store_abuseipdb_data(session, raw_data: list[dict]):
    repo = IOCRepository(session)
    for entry in raw_data:
        transformed = transform_abuseipdb_entry(entry)
        await repo.upsert_ioc(transformed)
    await repo.commit()
