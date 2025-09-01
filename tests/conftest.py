import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from app.db import Base
from dotenv import load_dotenv
import os

load_dotenv(".env.test")

TEST_DATABASE_URL = f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"


@pytest_asyncio.fixture(scope="function")
async def db_session():
    """Provide a clean async session per test."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async_session_local = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(
                text(f'TRUNCATE TABLE {table.name} RESTART IDENTITY CASCADE')
            )

    async with async_session_local() as session:
        yield session

    await engine.dispose()
