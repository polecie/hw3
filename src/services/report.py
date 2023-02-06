import dataclasses
import json
import uuid

from celery.result import AsyncResult
from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import FileResponse

from src.core.config import config
from src.db.cache import AbstractCache, get_report_cache
from src.db.db import get_async_session
from src.repositories.container import RepositoriesContainer
from src.services.mixin import ServiceMixin
from src.services.mock import AbstractMockData, get_mock_menu_service
from src.tasks.task import save_menu

__all__ = (
    "ReportService",
    "get_report_service",
)


@dataclasses.dataclass
class ReportService(ServiceMixin):
    mock_data: AbstractMockData

    async def put(self) -> dict:
        """Заполняет базу данных тестовыми данными."""
        mock_menu: list = await self.mock_data.create()
        report_status: bool = await self.container.report_repo.add(mock_data=mock_menu)
        if report_status is True:
            return {"status": report_status, "message": "The data has been added"}
        if report_status is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="not all data has been added or data has already been added",
            )
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
            if cached_report.decode("utf-8") == "SUCCESS":
                raise HTTPException(status_code=status.HTTP_200_OK, detail="the report was received")
            await self.cache.delete(key=f"{str(report_id)}")  # avoiding broken pipe error
            report_name = AsyncResult(str(report_id), app=save_menu)
            if report_name.ready():
                report: str = report_name.get()
                await self.cache.set(
                    key=f"{str(report_id)}", value=f"{report_name.status}", expire=config.report_cache_expire
                )
                filename = "menu-" + report.split("/")[-1]
                return FileResponse(
                    path=f"{report}",
                    filename=filename,
                    media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            await self.cache.set(
                key=f"{str(report_id)}", value=f"{report_name.status}", expire=config.report_cache_expire
            )
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail=f"the report is not yet ready, state is {report_name.status}",
            )
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="report not found")

    async def create(self) -> dict:
        """Запускает задачу по генерации отчета в excel-файл."""
        menu: str = await self.__get()
        response: AsyncResult = save_menu.delay(menu)
        if not response:
            pass
        await self.cache.set(key=f"{str(response.id)}", value=f"{response.status}", expire=config.report_cache_expire)
        return {"status": True, "message": f"The report {response.id} is processing"}


async def get_report_service(
    cache: AbstractCache = Depends(get_report_cache),
    session: AsyncSession = Depends(get_async_session),
    mock_data: AbstractMockData = Depends(get_mock_menu_service),
) -> ReportService:
    """Функция для внедрения зависимостей.

    :param mock_data: Сервис для генерации мок-данных.
    :param cache: Кеш.
    :param session: Асинхронная сессия с базой данных.
    """
    container = RepositoriesContainer(session=session)
    return ReportService(container=container, cache=cache, mock_data=mock_data)
