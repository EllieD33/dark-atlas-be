from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.repositories.ioc_repository import IOCRepository


async def list_iocs(
        session: AsyncSession,
        page: int = 1,
        limit: int = 1000
):
    repo = IOCRepository(session)
    iocs = await repo.get_iocs(page, limit)

    return iocs


async def list_iocs_in_range(
        session: AsyncSession,
        start_date: datetime,
        end_date: datetime,
        page: int = 1,
        limit: int = 1000
):
    repo = IOCRepository(session)
    iocs = await repo.get_iocs_by_date_range(start_date, end_date, page, limit)

    return iocs
