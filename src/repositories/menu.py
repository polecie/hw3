import uuid
from typing import Any

from sqlalchemy import distinct, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from src.api.v1.schemas.menu import MenuSchema
from src.models.models import Menu, Submenu
from src.repositories.base import AbstractRepository

__all__ = ("MenuRepository",)


class MenuRepository(AbstractRepository):
    model: type[Menu] = Menu

    async def list(
        self,
    ) -> list[dict[str, int | Any]]:
        """Возвращает записи всех меню, содержащиеся в базе данных."""
        statement = select(self.model).options(joinedload(self.model.submenus).joinedload(Submenu.dishes))
        async with self.session as session:
            async with session.begin():
                try:
                    response = (await session.execute(statement)).scalars()
                except Exception:
                    pass
        menus = [menu for menu in response.unique()]

        def __build(menu: Menu):
            return {
                "id": menu.id,
                "title": menu.title,
                "description": menu.description,
                "submenus_count": len(menu.submenus),
                "dishes_count": __count_dishes(menu),
            }

        def __count_dishes(menu: Menu):
            """Посчитать количество блюд в подменю определенного меню."""
            submenus = menu.submenus
            to_count = submenus
            output = 0
            for submenu in to_count:
                output += len(submenu.dishes)
            return output if output else 0

        return [__build(menu) for menu in menus]

    async def get(self, menu_id: uuid.UUID) -> Menu | None:
        """Возвращает запись меню по его `id`.

        :param menu_id: Идентификатор меню.
        """
        statement = (
            select(
                self.model.id,
                self.model.title,
                self.model.description,
                func.count(distinct(self.model.submenus)).label("submenus_count"),
                func.count(Submenu.dishes).label("dishes_count"),
            )
            .outerjoin(self.model.submenus)
            .outerjoin(Submenu.dishes)
            .where(self.model.id == menu_id)
            .group_by(self.model.id)
        )
        async with self.session as session:
            async with session.begin():
                try:
                    response = await session.execute(statement)
                except Exception:
                    pass
        menu: Menu | None = response.one_or_none()
        return menu

    async def __get(self, menu_id: uuid.UUID) -> Menu | None:
        statement = select(self.model).where(self.model.id == menu_id)
        async with self.session as session:
            async with session.begin():
                try:
                    response = await session.execute(statement)
                except Exception:
                    pass
        menu: Menu | None = response.scalar_one_or_none()
        return menu

    async def add(self, menu_content: MenuSchema) -> Menu | None:
        """Добавляет в базу данных новую запись меню.

        :param menu_content: Поля меню для добавления.
        """
        menu: Menu = Menu(**menu_content.dict())
        async with self.session as session:
            async with session.begin():
                try:
                    session.add(menu)
                except IntegrityError:
                    await session.rollback()
                else:
                    await session.commit()
            await session.refresh(menu)
        return menu

    async def update(self, menu_id: uuid.UUID, menu_content: MenuSchema) -> bool:
        """Обновляет запись меню по его `id`.

        :param menu_id: Идентификатор меню.
        :param menu_content: Поля меню, которые необходимо обновить.
        """
        menu_status = False
        if menu := await self.__get(menu_id=menu_id):
            updated_menu = menu_content.dict(exclude_unset=True)
            for key, value in updated_menu.items():
                setattr(menu, key, value)
            async with self.session as session:
                async with session.begin():
                    try:
                        session.add(menu)
                        menu_status = True
                    except Exception:
                        pass
                await session.refresh(menu)
        return menu_status

    async def delete(self, menu_id: uuid.UUID) -> bool:
        """Удаляет запись меню из базы данных по его `id`.

        :param menu_id: Идентификатор меню.
        """
        menu_status = False
        if menu := await self.__get(menu_id=menu_id):
            async with self.session as session:
                async with session.begin():
                    try:
                        await session.delete(menu)
                        await session.commit()
                        menu_status = True
                    except Exception:
                        pass
        return menu_status
