from datetime import timedelta, datetime, timezone

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.db import get_session
from app.models.ioc import IOC


@pytest.fixture
def override_get_session(db_session: AsyncSession):
    async def _override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = _override_get_session
    yield
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_list_iocs_endpoint(db_session, override_get_session):
    iocs = [IOC(type="ip", value=f"192.168.0.{i}", source="test") for i in range(5)]
    db_session.add_all(iocs)
    await db_session.commit()

    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://testserver"
    ) as client:
        response = await client.get("/iocs?page=1&limit=2")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


@pytest.mark.asyncio
async def test_list_iocs_in_range_endpoint(db_session, override_get_session):
    base_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
    iocs = [
        IOC(
            type="ip",
            value=f"10.0.0.{i}",
            source="test",
            last_seen=base_date + timedelta(days=i),
        )
        for i in range(5)
    ]
    db_session.add_all(iocs)
    await db_session.commit()

    start = base_date.isoformat()
    end = (base_date + timedelta(days=2)).isoformat()

    params = {
        "start_date": start,
        "end_date": end,
        "page": 1,
        "limit": 100
    }

    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://testserver"
    ) as client:
        response = await client.get("/iocs/range", params=params)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    expected_values = [f"10.0.0.{i}" for i in range(3)]
    actual_values = [ioc["value"] for ioc in data]
    assert actual_values == expected_values
