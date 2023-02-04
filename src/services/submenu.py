import json
import uuid

from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.schemas.submenu import SubmenuCreate, SubmenuResponse, SubmenuUpdate
from src.db.cache import AbstractCache, get_cache
from src.db.db import get_async_session
from src.repositories.container import RepositoriesContainer
from src.services.mixin import ServiceMixin

__all__ = (
    "SubmenuService",
    "get_submenu_service",
)


class SubmenuService(ServiceMixin):
    async def get_submenus(self, menu_id: uuid.UUID) -> list[SubmenuResponse]:
        """Возвращает список всех подменю, принадлежащих меню по `id` меню.

        :param menu_id: Идентификатор меню.
        """
        if cached_submenus := await self.cache.get(key="submenus"):
            return json.loads(cached_submenus)  # type: ignore
        submenus: list = await self.container.submenu_repo.list(menu_id=menu_id)
        cache = [SubmenuResponse.from_orm(submenu) for submenu in submenus]
        await self.cache.set(key="submenus", value=json.dumps(jsonable_encoder(cache)))
        return submenus

    async def get_submenu(self, submenu_id: uuid.UUID, menu_id: uuid.UUID) -> SubmenuResponse:
        """Возвращает подменю по его `id`.

        :param submenu_id: Идентификатор подменю.
        :param menu_id: Идентификатор меню.
        """
        if cached_submenu := await self.cache.get(key=f"{submenu_id}"):
            return json.loads(cached_submenu)  # type: ignore
        if submenu := await self.container.submenu_repo.get(submenu_id=submenu_id):
            submenu = SubmenuResponse.from_orm(submenu)
            await self.cache.set(
                key=f"{submenu_id}",
                value=json.dumps(jsonable_encoder(submenu)),
            )
            return submenu
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")

    async def create_submenu(self, submenu_content: SubmenuCreate, menu_id: uuid.UUID) -> SubmenuResponse:
        """Создает новое подменю.

        :param submenu_content: Поля для создания подменю.
        :param menu_id: Идентификатор меню.
        """
        cached_submenus = await self.cache.get(key="submenus")
        if cached_submenus:
            await self.cache.delete(key="submenus")
        submenu = await self.container.submenu_repo.add(submenu_content=submenu_content, menu_id=menu_id)
        return SubmenuResponse.from_orm(submenu)

    async def update_submenu(
        self,
        submenu_id: uuid.UUID,
        submenu_content: SubmenuUpdate,
        menu_id: uuid.UUID,
    ) -> SubmenuResponse:
        """Обновляет подменю.

        :param submenu_id: Идентификатор подменю.
        :param submenu_content: Поля для обновления подменю.
        :param menu_id: Идентификатор меню.
        """
        submenu_status: bool = await self.container.submenu_repo.update(
            submenu_id=submenu_id, submenu_content=submenu_content
        )
        if submenu_status is True:
            cached_submenus = await self.cache.get(key="submenus")
            if cached_submenus:
                await self.cache.delete(key="submenus")
            submenu = await self.container.submenu_repo.get(submenu_id)
            if await self.cache.get(key=f"{submenu_id}"):
                await self.cache.delete(f"{submenu_id}")
            submenu = SubmenuResponse.from_orm(submenu)
            await self.cache.set(
                key=f"{submenu_id}",
                value=json.dumps(jsonable_encoder(submenu)),
            )
            return submenu
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")

    async def delete_submenu(self, submenu_id: uuid.UUID, menu_id: uuid.UUID) -> dict:
        """Удаляет подменю по его `id`.

        :param submenu_id: Идентификатор подменю.
        :param menu_id: Идентификатор меню.
        """
        submenu_status: bool = await self.container.submenu_repo.delete(submenu_id=submenu_id)
        if submenu_status is True:
            await self.cache.flushall()
            return {
                "status": submenu_status,
                "message": "The submenu has been deleted",
            }
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")


async def get_submenu_service(
    cache: AbstractCache = Depends(get_cache),
    session: AsyncSession = Depends(get_async_session),
) -> SubmenuService:
    """Функция для внедрения зависимостей.

    :param cache: Кеш.
    :param session: Сессия с базой данных.
    """
    container = RepositoriesContainer(session=session)
    return SubmenuService(container=container, cache=cache)
