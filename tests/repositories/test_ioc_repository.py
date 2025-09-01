import pytest
from sqlalchemy import select
from datetime import datetime
from app.repositories.ioc_repository import IOCRepository
from app.models.ioc import IOC
from app.services.abuseipdb_service import transform_abuseipdb_entry


@pytest.mark.asyncio
async def test_upsert_and_commit(db_session):
    repo = IOCRepository(db_session)

    raw_entry = {
        "ipAddress": "192.168.0.1",
        "lastReportedAt": "2024-08-20T12:00:00Z"
    }

    ioc_data = transform_abuseipdb_entry(raw_entry)

    await repo.upsert_ioc(ioc_data)
    await repo.commit()

    result = await db_session.get(IOC, 1)  # Looking up primary key
    assert result is not None
    assert result.value == raw_entry['ipAddress']
    assert result.source == "AbuseIPDB"
    assert isinstance(result.last_seen, datetime)


@pytest.mark.asyncio
async def test_upsert_duplicate_does_not_raise(db_session):
    repo = IOCRepository(db_session)

    raw_entry = {
        "ipAddress": "10.0.0.5",
        "lastReportedAt": "2024-08-21T10:00:00Z"
    }
    ioc_data = transform_abuseipdb_entry(raw_entry)

    await repo.upsert_ioc(ioc_data)
    await repo.upsert_ioc(ioc_data)
    await repo.commit()

    result = await db_session.execute(select(IOC))
    rows = result.scalars().all()

    assert len(rows) == 1
    assert rows[0].value == raw_entry['ipAddress']
