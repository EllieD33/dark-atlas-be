import pytest
from sqlalchemy import select
from datetime import datetime, timedelta, timezone
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

@pytest.mark.asyncio
async def test_get_iocs(db_session):
    repo = IOCRepository(db_session)

    iocs = [
        IOC(type="ip", value=f"192.168.0.{i}", source="test")
        for i in range(25)
    ]
    db_session.add_all(iocs)
    await db_session.commit()

    result = await repo.get_iocs(2, 10)

    assert len(result) == 10
    assert isinstance(result[0], IOC)
    assert result[0].value == "192.168.0.10"


@pytest.mark.asyncio
async def test_get_iocs_by_date_range(db_session):
    repo = IOCRepository(db_session)

    base_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
    iocs = [
        IOC(
            type="ip",
            value=f"10.0.0.{i}",
            source="test",
            last_seen=base_date + timedelta(days=i)
        )
        for i in range(25)
    ]

    db_session.add_all(iocs)
    await db_session.commit()

    start_date = datetime(2024, 1, 5, tzinfo=timezone.utc)
    end_date = datetime(2024, 1, 10, tzinfo=timezone.utc)

    results = await repo.get_iocs_by_date_range(start_date, end_date, page=1, limit=100)

    assert all(start_date <= ioc.last_seen <= end_date for ioc in results)
    assert len(results) == 6