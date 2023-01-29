import json
import uuid

from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.schemas.dish import DishCreate, DishResponse, DishUpdate
from src.db.cache import AbstractCache, get_cache
from src.db.db import get_async_session
from src.repositories.container import RepositoriesContainer
from src.services.mixin import ServiceMixin


class DishService(ServiceMixin):
    async def get_dishes(
        self, menu_id: uuid.UUID, submenu_id: uuid.UUID
    ) -> list[DishResponse]:
        """

        :param menu_id: Идентификатор меню.
        :param submenu_id: Идентификатор подменю.
        """
        # проверить меню подменю
        # if cached_dishes := await self.cache.get(key="dishes"):
        #     return json.loads(cached_dishes)  # type: ignore
        dishes: list = await self.container.dish_repo.list(
            submenu_id=submenu_id
        )
        dishes = [DishResponse.from_orm(dish) for dish in dishes]
        return dishes

    async def get_dish(
        self, menu_id: uuid.UUID, submenu_id: uuid.UUID, dish_id: uuid.UUID
    ) -> DishResponse:
        """

        :param menu_id: Идентификатор меню.
        :param submenu_id: Идентификатор подменю.
        :param dish_id: Идентификатор блюда.
        """
        # проверить меню подменю
        if cached_dish := await self.cache.get(key=f"{dish_id}"):
            return json.loads(cached_dish)  # type: ignore
        if dish := await self.container.dish_repo.get(dish_id=dish_id):
            dish = DishResponse.from_orm(dish)
            await self.cache.set(
                key=f"{dish_id}", value=json.dumps(jsonable_encoder(dish))
            )
            return dish
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="dish not found"
        )

    async def create_dish(
        self,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_content: DishCreate,
    ) -> DishResponse:
        """

        :param menu_id: Идентификатор меню.
        :param submenu_id: Идентификатор подменю.
        :param dish_content: Поля для создания блюда.
        """
        # проверяем меню и подменю на существование
        dish = await self.container.dish_repo.add(
            dish_content=dish_content, submenu_id=submenu_id
        )
        return DishResponse.from_orm(dish)

    async def update_dish(
        self,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_id: uuid.UUID,
        dish_content: DishUpdate,
    ) -> DishResponse:
        """

        :param menu_id: Идентификатор меню.
        :param submenu_id: Идентификатор подменю.
        :param dish_id: Идентификатор блюда.
        :param dish_content: Поля для обновления блюда.
        """
        # проверяем меню и подменю
        dish_status: bool = await self.container.dish_repo.update(
            dish_id=dish_id, dish_content=dish_content
        )
        if dish_status is True:
            if await self.cache.get(key=f"{dish_id}"):
                await self.cache.delete(f"{dish_id}")
            dish = await self.container.dish_repo.get(dish_id)
            dish = DishResponse.from_orm(dish)
            await self.cache.set(
                key=f"{dish_id}", value=json.dumps(jsonable_encoder(dish))
            )
            return dish
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="dish not found"
        )

    async def delete_dish(
        self, menu_id: uuid.UUID, submenu_id: uuid.UUID, dish_id: uuid.UUID
    ) -> dict:
        """

        :param menu_id: Идентификатор меню.
        :param submenu_id: Идентификатор подменю.
        :param dish_id: Идентификатор блюда.
        """
        # проверить меню и подменю
        dish_status: bool = await self.container.dish_repo.delete(
            dish_id=dish_id
        )
        if dish_status is True:
            await self.cache.flushall()
            return {
                "status": dish_status,
                "message": "The dish has been deleted",
            }
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="dish not found"
        )


async def get_dish_service(
    cache: AbstractCache = Depends(get_cache),
    session: AsyncSession = Depends(get_async_session),
) -> DishService:
    """Функция для внедрения зависимостей.

    :param cache: Кеш.
    :param session: Сессия с базой данных.
    """
    container = RepositoriesContainer(session=session)
    return DishService(container=container, cache=cache)
