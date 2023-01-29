import uuid

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.cache import AbstractCache, get_cache
from src.db.db import get_async_session

from src.services.mixin import ServiceMixin
from src.repositories.container import RepositoriesContainer

from src.api.v1.schemas.dish import DishSchema, DishResponse


class DishService(ServiceMixin):
    async def get_dishes(self, menu_id: uuid.UUID, submenu_id: uuid.UUID) -> list[DishResponse]:
        """

        :param menu_id:
        :param submenu_id:
        :return:
        """
        ## проверить меню подменю
        dishes: list = await self.container.dish_repo.list(submenu_id=submenu_id)
        return dishes

    async def get_dish(self, menu_id: uuid.UUID, submenu_id: uuid.UUID, dish_id: uuid.UUID) -> DishResponse:
        """

        :param menu_id:
        :param submenu_id:
        :param dish_id:
        :return:
        """
        ## проверить меню подменю
        if dish := await self.container.dish_repo.get(dish_id=dish_id):
            return dish
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")

    async def create_dish(self, menu_id: uuid.UUID, submenu_id: uuid.UUID, dish_content: DishSchema) -> DishResponse:
        """

        :param menu_id:
        :param submenu_id:
        :param dish_content:
        :return:
        """
        # проверяем меню и подменю на существование
        dish = await self.container.dish_repo.add(dish_content=dish_content, submenu_id=submenu_id)
        return DishResponse.from_orm(dish)

    async def update_dish(self, menu_id: uuid.UUID, submenu_id: uuid.UUID, dish_id: uuid.UUID, dish_content: DishSchema) -> DishResponse:
        """

        :param menu_id:
        :param submenu_id:
        :param dish_id:
        :param dish_content:
        :return:
        """
        ## проверяем меню и подменю
        dish_status: bool = await self.container.dish_repo.update(dish_id=dish_id, dish_content=dish_content)
        if dish_status is True:
            dish = await self.container.dish_repo.get(dish_id)
            return dish
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")

    async def delete_dish(self, menu_id: uuid.UUID, submenu_id: uuid.UUID, dish_id: uuid.UUID) -> dict:
        """

        :param menu_id:
        :param submenu_id:
        :param dish_id:
        :return:
        """
        ## проверить меню и подменю
        dish_status: bool = await self.container.dish_repo.delete(dish_id=dish_id)
        if dish_status is True:
            return {"status": dish_status, "message": "The dish has been deleted"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")


async def get_dish_service(
        cache: AbstractCache = Depends(get_cache),
        session: AsyncSession = Depends(get_async_session),
) -> DishService:
    container = RepositoriesContainer(session=session)
    return DishService(container=container, cache=cache)
