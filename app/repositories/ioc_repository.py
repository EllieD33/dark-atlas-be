from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ioc import IOC


class IOCRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def upsert_ioc(self, ioc_data: dict) -> bool:
        stmt = (
            insert(IOC)
            .values(**ioc_data)
            .on_conflict_do_nothing(index_elements=["value"])
            .returning(IOC.value)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def bulk_upsert_iocs(self, iocs_data: list[dict]) -> None:
        if not iocs_data:
            return
        stmt = (
            insert(IOC)
            .values(iocs_data)
            .on_conflict_do_nothing(index_elements=["value"])
        )
        await self.session.execute(stmt)

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
