import dataclasses
import random
import uuid
from abc import ABC, abstractmethod

from src.api.v1.schemas.base import DishMock, MenuMock, SubmenuMock
from src.models.models import Dish, Menu, Submenu
from src.services.utils import descriptions, titles


class AbstractMockData(ABC):
    @abstractmethod
    async def create(self) -> list:
        raise NotImplementedError


@dataclasses.dataclass
class MockMenuService(AbstractMockData):
    menu: type[Menu] = Menu
    submenu: type[Submenu] = Submenu
    dish: type[Dish] = Dish

    menu_schema: type[MenuMock] = MenuMock
    submenu_schema: type[SubmenuMock] = SubmenuMock
    dish_schema: type[DishMock] = DishMock

    titles: list = titles
    descriptions: list = descriptions

    async def create(
        self,
    ) -> list:
        """Генерирует мок-данные меню."""
        mock = []
        for _ in range(random.randint(1, 5)):
            menu_id = uuid.uuid4()
            menu_data = {
                "id": menu_id,
                "title": random.choice(self.titles),
                "description": random.choice(self.descriptions),
            }
            submenu_data = [
                {
                    "id": uuid.uuid4(),
                    "title": random.choice(self.titles),
                    "description": random.choice(self.descriptions),
                    "menu_id": menu_id,
                }
                for _ in range(random.randint(0, 5))
            ]
            dish_data = [
                {
                    "id": uuid.uuid4(),
                    "title": random.choice(self.titles),
                    "description": random.choice(self.descriptions),
                    "price": random.uniform(0.0, 100.0),
                    "submenu_id": submenu["id"],
                }
                for submenu in submenu_data
                for _ in range(random.randint(0, 5))
            ]
            mock.append(self.menu(**dict(self.menu_schema(**menu_data))))
            mock.extend(self.submenu(**dict(self.submenu_schema(**submenu))) for submenu in submenu_data)
            mock.extend(self.dish(**dict(self.dish_schema(**dish))) for dish in dish_data)
        return mock


async def get_mock_menu_service() -> MockMenuService:
    """Функция для внедрения зависимостей."""
    return MockMenuService()
