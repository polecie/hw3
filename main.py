import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis import asyncio as aioredis

from src.api.v1.resources import dish, menu, report, submenu
from src.api.v1.schemas.tags import tags_metadata
from src.core.config import config
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
    debug=config.app_debug,
    openapi_tags=tags_metadata,
)


@app.get("/", summary="Тестовая ручка", description="Название и версия проекта")
async def root():
    """Название и версия проекта."""
    return {
        "service": config.app_name,
        "version": config.app_version,
        "description": config.app_description,
    }


@app.on_event("startup")
async def startup():
    """Подключаемся к бд при старте приложения."""
    redis_db0 = await aioredis.from_url(config.redis_url)
    redis_db1 = await aioredis.from_url(config.redis_report_url)
    cache.cache = redis_cache.CacheRedis(cache_instance=redis_db0)
    cache.report_cache = redis_cache.CacheRedis(cache_instance=redis_db1)


@app.on_event("shutdown")
async def shutdown():
    """Отключаемся от бд при завершении работы приложения."""
    await cache.cache.close()
    await cache.report_cache.close()


app.include_router(router=menu.router, prefix="/api/v1/menus", tags=["menus"])
app.include_router(router=submenu.router, prefix="/api/v1/menus", tags=["submenus"])
app.include_router(router=dish.router, prefix="/api/v1/menus", tags=["dishes"])
app.include_router(router=report.router, prefix="/api/v1/reports", tags=["reports"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
