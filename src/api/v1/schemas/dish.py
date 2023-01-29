from src.api.v1.schemas.base import BaseDish, BaseSchema


class DishBase(BaseSchema):
    """Базовая схема блюда."""


class DishSchema(DishBase):
    """Схема блюда."""

    price: float


class DishUpdate(DishSchema):
    class Config:
        schema_extra = {
            "examples": {
                "valid": {
                    "summary": "Верный формат запроса",
                    "description": "Ожидаемый формат данных для успешного ответа",
                    "value": {
                        "title": "My new dish",
                        "description": "Super cool menu for my restaurant",
                        "price": 3456.3456,
                    },
                },
                "invalid": {
                    "summary": "Неверный формат запроса",
                    "description": "Невалидные данные, которые приведут к ошибке валидации",
                    "value": {
                        "name": "",
                        "description": "My new dish description",
                        "amount": 345,
                    },
                },
            }
        }


class DishCreate(DishSchema):
    class Config:
        schema_extra = {
            "examples": {
                "valid": {
                    "summary": "Верный формат запроса",
                    "description": "Ожидаемый формат данных для успешного ответа",
                    "value": {
                        "title": "My new dish",
                        "description": "Super cool dish for my restaurant",
                        "price": 3456.3456,
                    },
                },
                "invalid": {
                    "summary": "Неверный формат запроса",
                    "description": "Невалидные данные, которые приведут к ошибке валидации",
                    "value": {
                        "name": "",
                        "description": "My new dish description",
                        "amount": 345,
                    },
                },
            }
        }


class DishResponse(BaseDish):
    """Схема блюда для ответа."""

    class Config:
        """Пример схемы для документации."""

        schema_extra = {
            "example": {
                "id": "602033b3-0462-4de1-a2f8-d8494795e0c0",
                "title": "Блюдо",
                "description": "Описание блюда",
                "price": "14.51",
            }
        }

        orm_mode = True
