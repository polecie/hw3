import json
import uuid

from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.schemas.menu import MenuCreate, MenuResponse, MenuUpdate
from src.db.cache import AbstractCache, get_cache
from src.db.db import get_async_session
from src.repositories.container import RepositoriesContainer
from src.services.mixin import ServiceMixin

__all__ = (
    "MenuService",
    "get_menu_service",
)


class MenuService(ServiceMixin):
    async def get_menus(self) -> list[MenuResponse]:
        """Возвращает список всех меню."""
        if cached_menus := await self.cache.get(key="menus"):
            return json.loads(cached_menus)  # type: ignore
        menus: list = await self.container.menu_repo.list()
        # cache = [MenuResponse.from_orm(menu) for menu in menus]
        await self.cache.set(key="menus", value=json.dumps(jsonable_encoder(menus)))
        return menus

    async def get_menu(self, menu_id: uuid.UUID) -> MenuResponse:
        """Возвращает меню по его `id`.

        :param menu_id: Идентификатор меню.
        """
        if cached_menu := await self.cache.get(key=f"{menu_id}"):
            return json.loads(cached_menu)  # type: ignore
        if menu := await self.container.menu_repo.get(menu_id=menu_id):
            menu = MenuResponse.from_orm(menu)
            await self.cache.set(key=f"{menu_id}", value=json.dumps(jsonable_encoder(menu)))
            return menu
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")

    async def create_menu(self, menu_content: MenuCreate) -> MenuResponse:
        """Создает новое меню.

        :param menu_content: Поля для создания меню.
        """
        cached_menus = await self.cache.get(key="menus")
        if cached_menus:
            await self.cache.delete(key="menus")
        menu = await self.container.menu_repo.add(menu_content=menu_content)
        return MenuResponse.from_orm(menu)

    async def update_menu(self, menu_id: uuid.UUID, menu_content: MenuUpdate) -> MenuResponse:
        """Обновляет меню.

        :param menu_id: Идентификатор меню.
        :param menu_content: Поля для обновления меню.
        """
        menu_status: bool = await self.container.menu_repo.update(menu_id=menu_id, menu_content=menu_content)
        if menu_status is True:
            cached_menus = await self.cache.get(key="menus")
            if cached_menus:
                await self.cache.delete(key="menus")
            menu = await self.container.menu_repo.get(menu_id)
            if await self.cache.get(key=f"{menu_id}"):
                await self.cache.delete(f"{menu_id}")
            menu = MenuResponse.from_orm(menu)
            await self.cache.set(key=f"{menu_id}", value=json.dumps(jsonable_encoder(menu)))
            return menu
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")

    async def delete_menu(self, menu_id: uuid.UUID) -> dict:
        """Удаляет меню по его `id`.

        :param menu_id: Идентификатор меню.
        """
        menu_status: bool = await self.container.menu_repo.delete(menu_id=menu_id)
        if menu_status is True:
            await self.cache.flushall()
            return {
                "status": menu_status,
                "message": "The menu has been deleted",
            }
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")


async def get_menu_service(
    cache: AbstractCache = Depends(get_cache),
    session: AsyncSession = Depends(get_async_session),
) -> MenuService:
    """Функция для внедрения зависимостей.

    :param cache: Кеш.
    :param session: Сессия с базой данных.
    """
    container = RepositoriesContainer(session=session)
    return MenuService(container=container, cache=cache)
