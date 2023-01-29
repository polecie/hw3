import uuid

from sqlalchemy import distinct, func, select

from src.api.v1.schemas.menu import MenuSchema
from src.models.models import Dish, Menu, Submenu
from src.repositories.base import AbstractRepository

__all__ = ("MenuRepository",)


class MenuRepository(AbstractRepository):
    """Репозиторий для работы с сущностью меню."""

    model: type[Menu] = Menu

    async def list(
        self,
    ) -> list[Menu]:
        """Возвращает записи всех меню, содержащиеся в базе данных."""
        statement = (
            select(
                self.model.id,
                self.model.title,
                self.model.description,
                func.count(distinct(self.model.submenus)).label(
                    "submenus_count"
                ),
                func.count(Submenu.dishes).label("dishes_count"),
            )
            .outerjoin(
                self.model.submenus,
            )
            .outerjoin(
                Dish,
                Dish.submenu_id == Submenu.id,  # type: ignore
            )
            .group_by(self.model.id)
        )
        async with self.session as session:
            async with session.begin():
                try:
                    response = await session.execute(statement)
                except Exception:
                    pass
        menu: Menu | None = response.all()  # type: ignore
        return menu

    async def get(self, menu_id: uuid.UUID) -> Menu | None:
        """Возвращает запись меню по его `id`.

        :param menu_id: Идентификатор меню.
        """
        statement = (
            select(
                self.model.id,
                self.model.title,
                self.model.description,
                func.count(distinct(self.model.submenus)).label(
                    "submenus_count"
                ),
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
                except Exception:
                    await session.rollback()
                else:
                    await session.commit()
            await session.refresh(menu)
        return menu

    async def update(
        self, menu_id: uuid.UUID, menu_content: MenuSchema
    ) -> bool:
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
