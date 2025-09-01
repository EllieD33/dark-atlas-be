from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ioc import IOC

class IOCRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def upsert_ioc(self, ioc_data: dict):
        stmt = (
            insert(IOC)
            .values(**ioc_data)
            .on_conflict_do_nothing(index_elements=["value"])
        )
        await self.session.execute(stmt)

    async def commit(self):
        await self.session.commit()

