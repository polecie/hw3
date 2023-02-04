import random
import uuid

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
                        "price": random.uniform(0.0, 100.0),
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
                        "price": random.uniform(0.0, 100.0),
                    },
                },
                "invalid": {
                    "summary": "Неверный формат запроса",
                    "description": "Невалидные данные, которые приведут к ошибке валидации",
                    "value": {
                        "title": "",
                        "description": "Описание нового блюда",
                        "amount": random.uniform(0.0, 100.0),
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
                "id": uuid.uuid4(),
                "title": "Блюдо",
                "description": "Описание блюда",
                "price": str(round(random.uniform(0.0, 100.0), 2)),
            }
        }

        orm_mode = True


dish_not_found_schema = {
    404: {
        "description": "Not Found",
        "content": {"application/json": {"example": {"detail": "dish not found"}}},
    }
}

delete_dish_schema = {
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "example": {
                    "status": True,
                    "message": "The dish has been deleted",
                }
            }
        },
    },
    404: {
        "description": "Not Found",
        "content": {"application/json": {"example": {"detail": "dish not found"}}},
    },
}

get_dishes_schema = {
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "empty": {"summary": "Пустой список блюд", "value": []},
                    "full": {
                        "summary": "В списке содержатся записи",
                        "value": [
                            {
                                "id": uuid.uuid4(),
                                "title": "Блюдо 1",
                                "description": "Описание блюда 1",
                                "price": str(round(random.uniform(0.0, 100.0), 2)),
                            },
                            {
                                "id": uuid.uuid4(),
                                "title": "Блюдо 2",
                                "description": "Описание блюда 2",
                                "price": str(round(random.uniform(0.0, 100.0), 2)),
                            },
                            {
                                "id": uuid.uuid4(),
                                "title": "Блюдо 3",
                                "description": "Описание блюда 3",
                                "price": str(round(random.uniform(0.0, 100.0), 2)),
                            },
                        ],
                    },
                }
            }
        },
    }
}
