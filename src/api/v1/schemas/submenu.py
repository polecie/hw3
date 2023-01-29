import uuid

from pydantic import BaseModel

from src.api.v1.schemas.base import BaseSchema


class SubmenuBase(BaseSchema):
    """Базовая схема подменю."""


class SubmenuSchema(SubmenuBase):
    """Схема подменю."""

    class Config:
        """Пример схемы для документации."""

        schema_extra = {
            "example": {
                "title": "Подменю",
                "description": "Описание подменю",
            }
        }


class SubmenuResponse(BaseModel):
    """Схема подменю для ответа."""

    id: uuid.UUID
    title: str
    description: str
    dishes_count: int = 0

    class Config:
        """Пример схемы подменю для документации."""

        schema_extra = {
            "example": {
                "id": "f2f48e47-49dd-45a9-9f8d-a04af3b0cc19",
                "title": "Подменю",
                "description": "Описание подменю",
                "dishes_count": 5,
            }
        }

        orm_mode = True
