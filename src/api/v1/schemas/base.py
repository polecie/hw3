import uuid

from pydantic import BaseModel, constr, validator


class BaseSchema(BaseModel):
    """Базовая схема для запросов."""

    title: constr(min_length=2, max_length=30)  # type: ignore
    description: constr(min_length=2, max_length=255)  # type: ignore


class BaseMenu(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    submenus_count: int = 0
    dishes_count: int = 0


class BaseSubmenu(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    dishes_count: int = 0


def set_price(cost: float) -> str:
    """Возвращает строковое представление цены блюда с двумя знаками после
    запятой."""
    return f"{cost:.2f}"


class BaseDish(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    price: float

    _price = validator("price", allow_reuse=True)(set_price)
