import json
import uuid

from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.schemas.menu import MenuResponse, MenuSchema
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
        """

        """

        menus: list = await self.container.menu_repo.list()
        return menus

    async def get_menu(self, menu_id: uuid.UUID) -> MenuResponse:
        """

        :param menu_id: Идентификатор меню.
        """
        if cached_menu := await self.cache.get(key=f"{menu_id}"):
            return json.loads(cached_menu)  # type: ignore
        if menu := await self.container.menu_repo.get(menu_id=menu_id):
            menu = MenuResponse.from_orm(menu)
            await self.cache.set(
                key=f"{menu_id}", value=json.dumps(jsonable_encoder(menu))
            )
            return menu
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="menu not found"
        )

    async def create_menu(self, menu_content: MenuSchema) -> MenuResponse:
        """

        :param menu_content: Поля для создания меню.
        """
        menu = await self.container.menu_repo.add(menu_content=menu_content)
        return MenuResponse.from_orm(menu)

    async def update_menu(
        self, menu_id: uuid.UUID, menu_content: MenuSchema
    ) -> MenuResponse:
        """

        :param menu_id: Идентификатор меню.
        :param menu_content: Поля для обновления меню.
        """
        menu_status: bool = await self.container.menu_repo.update(
            menu_id=menu_id, menu_content=menu_content
        )
        if menu_status is True:
            menu = await self.container.menu_repo.get(menu_id)
            if await self.cache.get(key=f"{menu_id}"):
                await self.cache.delete(f"{menu_id}")
            menu = MenuResponse.from_orm(menu)
            await self.cache.set(
                key=f"{menu_id}", value=json.dumps(jsonable_encoder(menu))
            )
            return menu
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="menu not found"
        )

    async def delete_menu(self, menu_id: uuid.UUID) -> dict:
        """

        :param menu_id: Идентификатор меню.
        """
        menu_status: bool = await self.container.menu_repo.delete(
            menu_id=menu_id
        )
        if menu_status is True:
            await self.cache.flushall()
            return {
                "status": menu_status,
                "message": "The menu has been deleted",
            }
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="menu not found"
        )


async def get_menu_service(
    cache: AbstractCache = Depends(get_cache),
    session: AsyncSession = Depends(get_async_session),
) -> MenuService:
    """
    Функция для внедрения зависимостей.
    :param cache: Кеш.
    :param session: Сессия с базой данных.
    """
    container = RepositoriesContainer(session=session)
    return MenuService(container=container, cache=cache)
