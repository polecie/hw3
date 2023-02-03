import asyncio
import re

import pytest
from httpx import AsyncClient
from redis import asyncio as aioredis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from main import app
from src.core import config
from src.db import cache, redis_cache
from src.db.db import base, get_async_session


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", name="engine", autouse=True)
async def engine():
    async_engine = create_async_engine(config.database_url)
    redis = await aioredis.from_url(config.redis_url)  # cache
    cache.cache = redis_cache.CacheRedis(cache_instance=redis)  # initializing cache
    # async with async_engine.begin() as conn:
    #     await conn.run_sync(base.metadata.create_all)
    with open("src/tests/mock_data.sql") as file:
        statements = re.split(r";\s*$", file.read(), flags=re.MULTILINE)
        for statement in statements:
            if statement:
                async with async_engine.begin() as conn:
                    await conn.execute(text(statement))
    yield async_engine
    async with async_engine.begin() as conn:
        await conn.run_sync(base.metadata.drop_all)


@pytest.fixture(scope="function", name="session")
async def session(engine):
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        yield session
    await session.close()


@pytest.fixture(scope="function", name="client")
async def client(session):
    app.dependency_overrides[get_async_session] = lambda: session
    async with AsyncClient(app=app, base_url="http://test/") as async_client:
        yield async_client
    app.dependency_overrides.clear()
