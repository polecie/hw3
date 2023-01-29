import uuid

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.cache import AbstractCache, get_cache
from src.db.db import get_async_session
from src.services.mixin import ServiceMixin
from src.repositories.container import RepositoriesContainer

from src.api.v1.schemas.menu import MenuSchema, MenuResponse

__all__ = ('MenuService', 'get_menu_service',)


class MenuService(ServiceMixin):
    async def get_menus(self) -> list[MenuResponse]:
        """

        :return:
        """

        menus: list = await self.container.menu_repo.list()
        return menus

    async def get_menu(self, menu_id: uuid.UUID) -> MenuResponse:
        """

        :param menu_id:
        :return:
        """
        if menu := await self.container.menu_repo.get(menu_id=menu_id):
            return MenuResponse.from_orm(menu)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")

    async def create_menu(self, menu_content: MenuSchema) -> MenuResponse:
        """

        :param menu_content:
        :return:
        """
        menu = await self.container.menu_repo.add(menu_content=menu_content)
        return MenuResponse.from_orm(menu)

    async def update_menu(self, menu_id: uuid.UUID, menu_content: MenuSchema) -> MenuResponse:
        """

        :param menu_id:
        :param menu_content:
        :return:
        """
        menu_status: bool = await self.container.menu_repo.update(menu_id=menu_id, menu_content=menu_content)
        if menu_status is True:
            menu = await self.container.menu_repo.get(menu_id)
            return MenuResponse.from_orm(menu)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")

    async def delete_menu(self, menu_id: uuid.UUID) -> dict:
        """

        :param menu_id:
        :return:
        """
        menu_status: bool = await self.container.menu_repo.delete(menu_id=menu_id)
        if menu_status is True:
            return {"status": menu_status, "message": "The menu has been deleted"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")


async def get_menu_service(
        cache: AbstractCache = Depends(get_cache),
        session: AsyncSession = Depends(get_async_session),
) -> MenuService:
    container = RepositoriesContainer(session=session)
    return MenuService(container=container, cache=cache)
