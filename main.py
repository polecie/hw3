import uvicorn
from redis import asyncio as aioredis
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.core import config
from src.api.v1.resources import menu, submenu, dish
from src.db import cache, redis_cache

app = FastAPI(
    title=config.app_name,
    description=config.app_description,
    version=config.app_version,
    # адрес документации в красивом интерфейсе
    docs_url="/api/openapi",
    redoc_url="/api/redoc",
    # адрес документации в формате openapi
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    debug=config.app_debug
)


@app.get("/", summary="Тестовая ручка")
async def root():
    """ Название и версия проекта """
    return {
        "service": config.app_name,
        "version": config.app_version,
        "description": config.app_description
    }


@app.on_event("startup")
async def startup():
    cache.cache = redis_cache.CacheRedis(
        cache_instance=await aioredis.Redis(
            host=config.redis_host, port=config.redis_port, max_connections=10))


@app.on_event("shutdown")
async def shutdown():
    await cache.cache.close()


app.include_router(router=menu.router, prefix="/api/v1/menus")
app.include_router(router=submenu.router, prefix="/api/v1/menus")
app.include_router(router=dish.router, prefix="/api/v1/menus")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.app_host,
        port=config.app_port
    )
