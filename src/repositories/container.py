from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.base import AbstractReport, AbstractRepository
from src.repositories.dish import DishRepository
from src.repositories.menu import MenuRepository
from src.repositories.report import ReportRepository
from src.repositories.submenu import SubmenuRepository


class AbstractRepositoriesContainer(ABC):
    menu_repo: AbstractRepository
    submenu_repo: AbstractRepository
    dish_repo: AbstractRepository
    report_repo: AbstractReport


class RepositoriesContainer(AbstractRepositoriesContainer):
    """Контейнер для хранения всех репозиториев и сессии для работы с ними."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.menu_repo: MenuRepository = MenuRepository(session=self.session)
        self.submenu_repo: SubmenuRepository = SubmenuRepository(session=self.session)
        self.dish_repo: DishRepository = DishRepository(session=self.session)
        self.report_repo: ReportRepository = ReportRepository(session=self.session)
