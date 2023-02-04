import random
import uuid

from src.api.v1.schemas.base import BaseSchema, BaseSubmenu


class SubmenuSchema(BaseSchema):
    """Схема подменю для обновления данных."""


class SubmenuResponse(BaseSubmenu):
    """Схема подменю для успешного ответа."""

    class Config:
        """Пример схемы подменю для документации."""

        schema_extra = {
            "example": {
                "id": uuid.uuid4(),
                "title": "Подменю",
                "description": "Описание подменю",
                "dishes_count": random.randint(0, 10),
            }
        }

        orm_mode = True


class SubmenuCreate(SubmenuSchema):
    """Схема подменю для создания нового подменю."""

    class Config:
        """Пример схемы подменю для документации."""

        schema_extra = {
            "examples": {
                "valid": {
                    "summary": "Верный формат запроса",
                    "description": "Ожидаемый формат данных для успешного ответа",
                    "value": {
                        "title": "Новое подменю",
                        "description": "Описание нового подменю",
                    },
                },
                "invalid": {
                    "summary": "Неверный формат запроса",
                    "description": "Невалидные данные, которые приведут к ошибке валидации",
                    "value": {
                        "title": "Но",
                        "description": "Описание нового подменю",
                    },
                },
            }
        }


class SubmenuUpdate(SubmenuSchema):
    """Схема подменю для обновления данных."""

    class Config:
        """Пример схемы подменю для документации."""

        schema_extra = {
            "examples": {
                "valid": {
                    "summary": "Верный формат запроса",
                    "description": "Ожидаемый формат данных для успешного ответа",
                    "value": {
                        "title": "Новое название",
                        "description": "Обновленное описание подменю",
                    },
                },
                "invalid": {
                    "summary": "Неверный формат запроса",
                    "description": "Невалидные данные, которые приведут к ошибке валидации",
                    "value": {
                        "name": "Новое название",
                        "description": "Обновленное описание подменю",
                    },
                },
            }
        }


submenu_not_found_schema = {
    404: {
        "description": "Not Found",
        "content": {"application/json": {"example": {"detail": "submenu not found"}}},
    }
}

delete_submenu_schema = {
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "example": {
                    "status": True,
                    "message": "The submenu has been deleted",
                }
            }
        },
    },
    404: {
        "description": "Not Found",
        "content": {"application/json": {"example": {"detail": "submenu not found"}}},
    },
}

get_submenus_schema = {
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "empty": {"summary": "Пустой список подменю", "value": []},
                    "full": {
                        "summary": "В списке содержатся записи",
                        "value": [
                            {
                                "id": uuid.uuid4(),
                                "title": "Подменю 1",
                                "description": "Описание подменю 1",
                                "dishes_count": random.randint(0, 10),
                            },
                            {
                                "id": uuid.uuid4(),
                                "title": "Подменю 2",
                                "description": "Описание подменю 2",
                                "dishes_count": random.randint(0, 10),
                            },
                            {
                                "id": uuid.uuid4(),
                                "title": "Подменю 3",
                                "description": "Описание подменю 3",
                                "dishes_count": random.randint(0, 10),
                            },
                        ],
                    },
                }
            }
        },
    }
}
