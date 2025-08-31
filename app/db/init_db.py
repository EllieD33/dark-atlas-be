import asyncio
from app.db import engine, Base
from app.models.ioc import IOC


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created!")


if __name__ == "__main__":
    asyncio.run(init_db())
