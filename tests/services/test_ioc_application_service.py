import pytest
from datetime import datetime, timezone
from app.models.ioc import IOC
from app.services.ioc_application_service import store_abuseipdb_data


@pytest.mark.asyncio
async def test_store_abuseipdb_data(db_session):
    raw_data = [
        {"ipAddress": "1.2.3.4", "lastReportedAt": "2025-09-20T12:00:00Z"},
        {"ipAddress": "5.6.7.8"},
    ]

    await store_abuseipdb_data(db_session, raw_data)

    result = (await db_session.execute(
        IOC.__table__.select()
    )).fetchall()

    assert len(result) == 2

    first_row = result[0]
    assert first_row.value == "1.2.3.4"
    assert first_row.type == "ip"
    assert first_row.last_seen == datetime(2025, 9, 20, 12, 0, tzinfo=timezone.utc)

    second_row = result[1]
    assert second_row.value == "5.6.7.8"
    assert second_row.last_seen is None
