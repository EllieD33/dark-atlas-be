from datetime import datetime, timezone, timedelta

import pytest
from app.models.ioc import IOC
from app.services.ioc_service import list_iocs, list_iocs_in_range


@pytest.mark.asyncio
async def test_list_iocs_returns_paginated_results(db_session):
    iocs = [
        IOC(type="ip", value=f"192.168.0.{i}", source="test")
        for i in range(25)
    ]
    db_session.add_all(iocs)
    await db_session.commit()

    result = await list_iocs(db_session, page=2, limit=10)

    assert len(result) == 10
    assert result[0].value == "192.168.0.10"
    assert result[-1].value == "192.168.0.19"


@pytest.mark.asyncio
async def test_list_iocs_page_out_of_range_returns_empty(db_session):
    iocs = [
        IOC(type="ip", value=f"10.0.0.{i}", source="test")
        for i in range(5)
    ]
    db_session.add_all(iocs)
    await db_session.commit()

    result = await list_iocs(db_session, page=10, limit=10)

    assert result == []


@pytest.mark.asyncio
async def test_list_iocs_in_range(db_session):
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

    start_date = base_date + timedelta(days=5)
    end_date = base_date + timedelta(days=14)
    result = await list_iocs_in_range(db_session, start_date, end_date, page=1, limit=100)

    assert len(result) == 10
    assert all(start_date <= ioc.last_seen <= end_date for ioc in result)


@pytest.mark.asyncio
async def test_list_iocs_in_range_no_results(db_session):
    base_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
    iocs = [
        IOC(
            type="ip",
            value=f"10.0.0.{i}",
            source="test",
            last_seen=base_date + timedelta(days=i)
        )
        for i in range(10)
    ]
    db_session.add_all(iocs)
    await db_session.commit()

    start_date = datetime(2023, 1, 1, tzinfo=timezone.utc)
    end_date = datetime(2023, 1, 10, tzinfo=timezone.utc)
    result = await list_iocs_in_range(db_session, start_date, end_date, page=1, limit=100)

    assert result == []


@pytest.mark.asyncio
async def test_list_iocs_in_range_with_pagination(db_session):
    base_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
    iocs = [
        IOC(
            type="ip",
            value=f"172.16.0.{i}",
            source="test",
            last_seen=base_date + timedelta(days=i)
        )
        for i in range(15)
    ]
    db_session.add_all(iocs)
    await db_session.commit()

    start_date = base_date
    end_date = base_date + timedelta(days=14)
    page_1 = await list_iocs_in_range(db_session, start_date, end_date, page=1, limit=5)
    page_2 = await list_iocs_in_range(db_session, start_date, end_date, page=2, limit=5)
    page_3 = await list_iocs_in_range(db_session, start_date, end_date, page=3, limit=5)

    assert len(page_1) == 5
    assert len(page_2) == 5
    assert len(page_3) == 5
    assert page_1[0].value == "172.16.0.0"
    assert page_2[0].value == "172.16.0.5"
    assert page_3[0].value == "172.16.0.10"
