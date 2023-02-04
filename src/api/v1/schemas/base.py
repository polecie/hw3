import uuid

from pydantic import BaseModel, constr, validator


def set_price(cost: float) -> str:
    """Возвращает строковое представление цены блюда с двумя знаками после
    запятой."""
    return f"{cost:.2f}"


class BaseSchema(BaseModel):
    """Базовая схема для запросов."""

    title: constr(min_length=2, max_length=30)  # type: ignore
    description: constr(min_length=2, max_length=255)  # type: ignore


class ReportBase(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class ReportDish(ReportBase):
    price: float

    _price = validator("price", allow_reuse=True)(set_price)

    class Config:
        orm_mode = True


class ReportSubmenu(ReportBase):
    dishes: list[ReportDish]

    class Config:
        orm_mode = True


class ReportMenu(ReportBase):
    submenus: list[ReportSubmenu]

    class Config:
        orm_mode = True


class ReportSchema(ReportMenu):
    ...


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


class BaseDish(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    price: float

    _price = validator("price", allow_reuse=True)(set_price)


class Mock(BaseModel):
    id: uuid.UUID
    title: str
    description: str

    class Config:
        orm_mode = True


class MenuMock(Mock):
    ...


class SubmenuMock(Mock):
    menu_id: uuid.UUID


class DishMock(Mock):
    id: uuid.UUID
    title: str
    description: str
    price: float
    submenu_id: uuid.UUID
