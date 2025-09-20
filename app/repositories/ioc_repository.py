from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ioc import IOC
from datetime import datetime


class IOCRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def upsert_ioc(self, ioc_data: dict) -> bool:
        try:
            stmt = (
                insert(IOC)
                .values(**ioc_data)
                .on_conflict_do_nothing(index_elements=["value"])
                .returning(IOC.value)
            )
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none() is not None
        except Exception:
            await self.session.rollback()
            raise

    async def bulk_upsert_iocs(self, iocs_data: list[dict]) -> None:
        if not iocs_data:
            return
        try:
            stmt = (
                insert(IOC)
                .values(iocs_data)
                .on_conflict_do_nothing(index_elements=["value"])
            )
            await self.session.execute(stmt)
        except Exception:
            await self.session.rollback()
            raise

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def get_iocs(self, page: int, limit: int) -> list[IOC]:
        stmt = select(IOC).offset((page - 1) * limit).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_iocs_by_date_range(self, start_date: datetime, end_date: datetime, page: int,
                                     limit: int) -> list[IOC]:
        stmt = (
            select(IOC).where(IOC.last_seen >= start_date, IOC.last_seen <= end_date).offset((page - 1) * limit).limit(
                limit))
        result = await self.session.execute(stmt)
        return result.scalars().all()
