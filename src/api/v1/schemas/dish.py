import uuid

from pydantic import BaseModel, validator

from src.api.v1.schemas.base import BaseSchema


class DishBase(BaseSchema):
    """Базовая схема блюда"""


class DishSchema(DishBase):
    """Схема блюда"""

    price: float

    class Config:
        """Пример схемы для документации"""

        schema_extra = {
            "example": {
                "title": "Блюдо",
                "description": "Описание блюда",
                "price": "14.51456",
            }
        }


def set_price(cost: float) -> str:
    """
    Функция возвращает строковое представление
    цены блюда с двумя знаками после запятой
    """
    return f"{cost:.2f}"


class DishResponse(BaseModel):
    """Схема блюда для ответа"""

    id: uuid.UUID
    title: str
    description: str
    price: float

    _price = validator("price", allow_reuse=True)(set_price)

    class Config:
        """Пример схемы для документации"""

        schema_extra = {
            "example": {
                "id": "602033b3-0462-4de1-a2f8-d8494795e0c0",
                "title": "Блюдо",
                "description": "Описание блюда",
                "price": "14.51",
            }
        }

        orm_mode = True
