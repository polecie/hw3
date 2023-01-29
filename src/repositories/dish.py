import uuid

from src.repositories.base import AbstractRepository
from src.models.models import Dish
from src.api.v1.schemas.dish import DishSchema

from sqlalchemy import select


class DishRepository(AbstractRepository):
    model: type[Dish] = Dish

    async def list(self, submenu_id: uuid.UUID) -> list[Dish]:
        """

        :param submenu_id:
        :return:
        """
        statement = select(
            self.model.id,
            self.model.title,
            self.model.description,
            self.model.price
        ).where(self.model.submenu_id == submenu_id)
        async with self.session as session:
            async with session.begin():
                try:
                    response = await session.execute(statement)
                except Exception:
                    pass
            dish: list[Dish] = response.all()  # type: ignore
        return dish

    async def get(self, dish_id: uuid.UUID) -> Dish | None:
        """

        :param dish_id:
        :return:
        """
        statement = select(
            self.model.id,
            self.model.title,
            self.model.description,
            self.model.price
        ).where(self.model.id == dish_id)
        async with self.session as session:
            async with session.begin():
                try:
                    response = await session.execute(statement)
                except Exception:
                    pass
            dish: Dish | None = response.one_or_none()
        return dish

    async def __get(self, dish_id: uuid.UUID) -> Dish | None:
        statement = select(self.model).where(self.model.id == dish_id)
        async with self.session as session:
            async with session.begin():
                try:
                    response = await session.execute(statement)
                except Exception:
                    pass
        dish: Dish | None = response.scalar_one_or_none()
        return dish

    async def add(self, dish_content: DishSchema, submenu_id: uuid.UUID) -> Dish | None:
        """

        :param dish_content:
        :param submenu_id:
        :return:
        """
        new_dish = dish_content.dict(exclude_unset=True)
        new_dish["submenu_id"] = submenu_id
        dish: Dish = Dish(**new_dish)
        async with self.session as session:
            async with session.begin():
                try:
                    session.add(dish)
                except Exception:
                    await session.rollback()
                else:
                    await session.commit()
            await session.refresh(dish)
        return dish

    async def update(self, dish_id: uuid.UUID, dish_content: DishSchema) -> bool:
        """

        :param dish_id:
        :param dish_content:
        :return:
        """
        dish_status = False
        if dish := await self.__get(dish_id=dish_id):
            updated_dish = dish_content.dict(exclude_unset=True)
            for key, value in updated_dish.items():
                setattr(dish, key, value)
            async with self.session as session:
                async with session.begin():
                    try:
                        session.add(dish)
                        dish_status = True
                    except Exception:
                        pass
                await session.refresh(dish)
        return dish_status

    async def delete(self, dish_id: uuid.UUID) -> bool:
        """

        :param dish_id:
        :return:
        """
        dish_status = False
        if dish := await self.__get(dish_id=dish_id):
            async with self.session as session:
                async with session.begin():
                    try:
                        await session.delete(dish)
                        await session.commit()
                        dish_status = True
                    except Exception:
                        pass
        return dish_status
