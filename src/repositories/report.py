from sqlalchemy import select

# from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from src.api.v1.schemas.base import ReportSchema
from src.models.models import Menu, Submenu
from src.repositories.base import AbstractReport

__all__ = ("ReportRepository",)


class ReportRepository(AbstractReport):
    """"""

    async def get(self):
        """"""
        statement = select(Menu).options(joinedload(Menu.submenus).joinedload(Submenu.dishes))
        async with self.session as session:
            async with session.begin():
                response = (await session.execute(statement)).scalars()
        menus = [ReportSchema.from_orm(menu) for menu in response.unique()]
        return menus

    async def add(self, mock_data: list) -> bool:
        """"""
        status = False
        mock = (i for i in mock_data)
        while True:
            try:
                item = next(mock)
                self.session.add(item)
                await self.session.commit()
                await self.session.refresh(item)
                status = True
            except StopIteration:
                break
        return status
