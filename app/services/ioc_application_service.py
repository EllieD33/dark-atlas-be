from app.services.abuseipdb_service import transform_abuseipdb_entry
from app.repositories.ioc_repository import IOCRepository
from app.services.urlhaus_service import transform_urlhaus_entry


async def store_abuseipdb_data(session, raw_data: list[dict]):
    repo = IOCRepository(session)
    for entry in raw_data:
        transformed = transform_abuseipdb_entry(entry)
        await repo.upsert_ioc(transformed)
    await repo.commit()


async def store_urlhaus_data(session, raw_data: list[tuple[str, list[dict]]]):
    repo = IOCRepository(session)
    for entry_id, reports in raw_data:
        transformed_list = transform_urlhaus_entry(entry_id, reports)
        for transformed in transformed_list:
            await repo.upsert_ioc(transformed)
    await repo.commit()
