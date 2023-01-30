from src.api.v1.schemas.base import BaseDish, BaseSchema


class DishSchema(BaseSchema):
    """Схема блюда для обновления данных."""

    price: float


class DishUpdate(DishSchema):
    """Схема для обновлен нового блюда."""

    class Config:
        """Пример схемы для документации."""

        schema_extra = {
            "examples": {
                "valid": {
                    "summary": "Верный формат запроса",
                    "description": "Ожидаемый формат данных для успешного ответа",
                    "value": {
                        "title": "Измененное название",
                        "description": "Новое описание",
                        "price": 3456.3456,
                    },
                },
                "invalid": {
                    "summary": "Неверный формат запроса",
                    "description": "Невалидные данные, которые приведут к ошибке валидации",
                    "value": {
                        "title": "Новое название",
                        "description": "Измененное описание",
                        "price": "Сто",
                    },
                },
            }
        }


class DishCreate(DishSchema):
    """Схема для создания нового блюда."""

    class Config:
        """Пример схемы для документации."""

        schema_extra = {
            "examples": {
                "valid": {
                    "summary": "Верный формат запроса",
                    "description": "Ожидаемый формат данных для успешного ответа",
                    "value": {
                        "title": "Новое блюдо",
                        "description": "Описание нового блюда",
                        "price": 3456.3456,
                    },
                },
                "invalid": {
                    "summary": "Неверный формат запроса",
                    "description": "Невалидные данные, которые приведут к ошибке валидации",
                    "value": {
                        "title": "",
                        "description": "Описание нового блюда",
                        "amount": 345.45,
                    },
                },
            }
        }


class DishResponse(BaseDish):
    """Схема блюда для успешного ответа."""

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
