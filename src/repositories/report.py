import re

from sqlalchemy import select, text
from sqlalchemy.orm import joinedload

from src.api.v1.schemas.base import ReportSchema
from src.models.models import Menu, Submenu
from src.repositories.base import AbstractReport

__all__ = ("ReportRepository",)


class ReportRepository(AbstractReport):
    async def get(self):
        statement = select(Menu).options(joinedload(Menu.submenus).joinedload(Submenu.dishes))
        async with self.session as session:
            async with session.begin():
                response = (await session.execute(statement)).scalars()
        menus = [ReportSchema.from_orm(menu) for menu in response.unique()]
        return menus

    async def put(self) -> bool:
        status = False
        with open("src/tasks/menu.sql") as file:
            statements = re.split(r";\s*$", file.read(), flags=re.MULTILINE)
            for statement in statements:
                if statement:
                    async with self.session as session:
                        async with session.begin():
                            try:
                                status = True
                                await session.execute(text(statement))
                            except Exception:
                                pass
        return status
