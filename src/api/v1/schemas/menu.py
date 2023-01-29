import uuid

from pydantic import BaseModel

from src.api.v1.schemas.base import BaseSchema


class MenuBase(BaseSchema):
    """Базовая схема меню"""


class MenuSchema(MenuBase):
    """Схема меню"""

    class Config:
        """Пример схемы меню для документации"""

        schema_extra = {
            "example": {
                "title": "Меню",
                "description": "Описание меню",
            }
        }


class MenuResponse(BaseModel):
    """Схема меню ответа"""

    id: uuid.UUID
    title: str
    description: str
    submenus_count: int = 0
    dishes_count: int = 0

    class Config:
        """Пример схемы меню для документации"""

        schema_extra = {
            "example": {
                "id": "9202923d-afd2-4b4d-acb9-7d4c4f9bcc3a",
                "title": "Меню",
                "description": "Описание меню",
                "submenus_count": 3,
                "dishes_count": 0,
            }
        }

        orm_mode = True
