from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.core.config import config

base = declarative_base()

async_engine = create_async_engine(config.database_url, future=True, echo=False)


async def get_async_session():
    """Асинхронная сессия для работы в бд."""
    async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)  # type: ignore
    async with async_session() as session:
        yield session
