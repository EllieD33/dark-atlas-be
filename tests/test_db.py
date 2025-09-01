import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ioc import IOC

@pytest.mark.asyncio
async def test_db_connection(db_session):
    result = await db_session.execute(text("SELECT 1"))
    assert result.scalar() == 1

@pytest.mark.asyncio
async def test_insert_ioc(db_session):
    ioc = IOC(type="ip", value="1.2.3.4", source="test-feed")
    db_session.add(ioc)
    await db_session.commit()
    retrieved = await db_session.get(IOC, ioc.id)
    assert retrieved.value == "1.2.3.4"
    assert retrieved.type == "ip"

@pytest.mark.asyncio
async def test_unique_value_constraint(db_session):
    ioc1 = IOC(type="ip", value="9.8.7.6", source="feed1")
    ioc2 = IOC(type="ip", value="9.8.7.6", source="feed2")
    db_session.add(ioc1)
    await db_session.commit()
    db_session.add(ioc2)
    with pytest.raises(IntegrityError):
        try:
            await db_session.commit()
        finally:
            await db_session.rollback()
