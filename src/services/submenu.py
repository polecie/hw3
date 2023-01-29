import uuid

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.cache import AbstractCache, get_cache
from src.db.db import get_async_session
from src.services.mixin import ServiceMixin
from src.repositories.container import RepositoriesContainer

from src.api.v1.schemas.submenu import SubmenuSchema, SubmenuResponse


__all__ = ('SubmenuService', 'get_submenu_service',)


class SubmenuService(ServiceMixin):

    async def get_submenus(self, menu_id: uuid.UUID) -> list[SubmenuResponse]:
        """

        :param menu_id:
        :return:
        """
        ## проверить меню
        submenus: list = await self.container.submenu_repo.list(menu_id=menu_id)
        return submenus

    async def get_submenu(self, submenu_id: uuid.UUID, menu_id: uuid.UUID) -> SubmenuResponse:
        """

        :param submenu_id:
        :param menu_id:
        :return:
        """
        ## проверить меню
        if submenu := await self.container.submenu_repo.get(submenu_id=submenu_id):
            return submenu
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")

    async def create_submenu(self, submenu_content: SubmenuSchema, menu_id: uuid.UUID) -> SubmenuResponse:
        """

        :param submenu_content:
        :param menu_id:
        :return:
        """
        # проверяем меню на существование
        submenu = await self.container.submenu_repo.add(submenu_content=submenu_content, menu_id=menu_id)
        return SubmenuResponse.from_orm(submenu)

    async def update_submenu(self, submenu_id: uuid.UUID, submenu_content: SubmenuSchema, menu_id: uuid.UUID) -> SubmenuResponse:
        """

        :param submenu_id:
        :param submenu_content:
        :param menu_id:
        :return:
        """
        ## проверяем меню
        submenu_status: bool = await self.container.submenu_repo.update(submenu_id=submenu_id, submenu_content=submenu_content)
        if submenu_status is True:
            submenu = await self.container.submenu_repo.get(submenu_id)
            return submenu
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")

    async def delete_submenu(self, submenu_id: uuid.UUID, menu_id: uuid.UUID) -> dict:
        """

        :param submenu_id:
        :param menu_id:
        :return:
        """
        ## проверить меню
        submenu_status: bool = await self.container.submenu_repo.delete(submenu_id=submenu_id)
        if submenu_status is True:
            return {"status": submenu_status, "message": "The submenu has been deleted"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")


async def get_submenu_service(
        cache: AbstractCache = Depends(get_cache),
        session: AsyncSession = Depends(get_async_session),
) -> SubmenuService:
    container = RepositoriesContainer(session=session)
    return SubmenuService(container=container, cache=cache)
