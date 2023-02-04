import json
import uuid

from celery.result import AsyncResult
from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import FileResponse

from src.db.cache import AbstractCache, get_report_cache
from src.db.db import get_async_session
from src.repositories.container import RepositoriesContainer
from src.services.mixin import ServiceMixin
from src.tasks.task import save_menu

__all__ = (
    "ReportService",
    "get_report_service",
)


class ReportService(ServiceMixin):
    async def put(self) -> dict:
        """Заполняет базу данных тестовыми данными."""
        report_status: bool = await self.container.report_repo.add()
        if report_status is True:
            return {"status": report_status, "message": "The data has been added"}
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="data has not been added",
        )

    async def __get(self) -> str:
        menus = await self.container.report_repo.get()
        menus = json.dumps(jsonable_encoder(menus))
        return menus

    async def get(self, report_id: uuid.UUID):
        """Возвращает список меню из базы данных для формирования отчета."""
        cached_report = await self.cache.get(f"{str(report_id)}")
        if cached_report:
            await self.cache.delete(key=f"{str(report_id)}")  # avoiding broken pipe error
            report_name = AsyncResult(str(report_id), app=save_menu)
            report: str = report_name.get()
            return FileResponse(path=f"{report}", filename=report, media_type="multipart/form-data")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="report not found")

    async def create(self) -> dict:
        """"""
        menu: str = await self.__get()
        response: AsyncResult = save_menu.delay(menu)
        if not response:
            pass
        await self.cache.set(key=f"{str(response.id)}", value="OK")
        return {"id": response.id}


async def get_report_service(
    cache: AbstractCache = Depends(get_report_cache),
    session: AsyncSession = Depends(get_async_session),
) -> ReportService:
    """Функция для внедрения зависимостей.

    :param cache: Кеш.
    :param session: Асинхронная сессия с базой данных.
    """
    container = RepositoriesContainer(session=session)
    return ReportService(container=container, cache=cache)
