import json

from fastapi import Depends, HTTPException
from fastapi import status as response_status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_async_session
from src.repositories.container import RepositoriesContainer
from src.services.mixin import Service


class ReportService(Service):
    async def put(self) -> dict:
        """Заполняет базу данных тестовыми данными."""
        status: bool = await self.container.report_repo.put()
        if status is True:
            return {"status": status, "message": "The data has been added"}
        raise HTTPException(
            status_code=response_status.HTTP_400_BAD_REQUEST,
            detail="cannot add data to database",
        )

    async def get(self) -> str:
        """Возвращает список меню из базы данных для формирования отчета."""
        menus = await self.container.report_repo.get()
        menus = json.dumps(jsonable_encoder(menus))
        return menus


async def get_report_service(
    session: AsyncSession = Depends(get_async_session),
) -> ReportService:
    """Функция для внедрения зависисмостей.

    :param session: Асинхронная сессия с базой данных.
    """
    container = RepositoriesContainer(session=session)
    return ReportService(container=container)
