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


dish_not_found_schema = {
    404: {
        "description": "Not Found",
        "content": {
            "application/json": {"example": {"detail": "dish not found"}}
        },
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
        "content": {
            "application/json": {"example": {"detail": "dish not found"}}
        },
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
                                "id": "9202923d-afd2-4b4d-acb9-7d4c4f9bcc3a",
                                "title": "Блюдо 1",
                                "description": "Описание блюда 1",
                                "price": "1.34",
                            },
                            {
                                "id": "779254bb-f0bd-4899-804e-0cb925d88621",
                                "title": "Блюдо 2",
                                "description": "Описание блюда 2",
                                "price": "23.12",
                            },
                            {
                                "id": "781f9966-587a-49ed-a095-d10f5fe6ecf6",
                                "title": "Блюдо 3",
                                "description": "Описание блюда 3",
                                "price": "9.34",
                            },
                        ],
                    },
                }
            }
        },
    }
}
