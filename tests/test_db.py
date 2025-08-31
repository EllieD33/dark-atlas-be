import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ioc import IOC

@pytest.mark.asyncio
async def test_db_connection(session: AsyncSession):
    result = await session.execute(text("SELECT 1"))
    assert result.scalar() == 1

@pytest.mark.asyncio
async def test_insert_ioc(session: AsyncSession):
    ioc = IOC(type="ip", value="1.2.3.4", source="test-feed")
    session.add(ioc)
    await session.commit()
    retrieved = await session.get(IOC, ioc.id)
    assert retrieved.value == "1.2.3.4"
    assert retrieved.type == "ip"

@pytest.mark.asyncio
async def test_unique_value_constraint(session: AsyncSession):
    ioc1 = IOC(type="ip", value="9.8.7.6", source="feed1")
    ioc2 = IOC(type="ip", value="9.8.7.6", source="feed2")
    session.add(ioc1)
    await session.commit()
    session.add(ioc2)
    with pytest.raises(IntegrityError):
        try:
            await session.commit()
        finally:
            await session.rollback()
