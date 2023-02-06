import random
import uuid

from src.api.v1.schemas.base import BaseMenu, BaseSchema


class MenuSchema(BaseSchema):
    """Схема меню для обновления данных."""
    # class Config:
    #     orm_mode = True


class MenuResponse(BaseMenu):
    """Схема меню для успешного ответа."""

    class Config:
        """Пример схемы меню для документации."""

        schema_extra = {
            "example": {
                "id": uuid.uuid4(),
                "title": "Меню",
                "description": "Описание меню",
                "submenus_count": random.randint(0, 10),
                "dishes_count": random.randint(0, 10),
            }
        }

        orm_mode = True


class MenuCreate(MenuSchema):
    """Схема для создания нового меню."""

    class Config:
        """Пример схемы меню для документации."""

        schema_extra = {
            "examples": {
                "valid": {
                    "summary": "Верный формат запроса",
                    "description": "Ожидаемый формат данных для успешного ответа",
                    "value": {
                        "title": "Название меню",
                        "description": "Описание нового меню",
                    },
                },
                "invalid": {
                    "summary": "Неверный формат запроса",
                    "description": "Невалидные данные, которые приведут к ошибке валидации",
                    "value": {
                        "name": "Новое меню",
                        "description": "Описание нового меню",
                    },
                },
            }
        }


class MenuUpdate(MenuSchema):
    """Схема для изменения меню."""

    class Config:
        """Пример схемы меню для документации."""

        schema_extra = {
            "examples": {
                "valid": {
                    "summary": "Верный формат запроса",
                    "description": "Ожидаемый формат данных для успешного ответа",
                    "value": {
                        "title": "Новое название",
                        "description": "Обновленное описание меню",
                    },
                },
                "invalid": {
                    "summary": "Неверный формат запроса",
                    "description": "Невалидные данные, которые приведут к ошибке валидации",
                    "value": {
                        "title": "F",
                        "description": "Обновленное описание меню",
                    },
                },
            }
        }


menu_not_found_schema = {
    404: {
        "description": "Not Found",
        "content": {"application/json": {"example": {"detail": "menu not found"}}},
    }
}

delete_menu_schema = {
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "example": {
                    "status": True,
                    "message": "The menu has been deleted",
                }
            }
        },
    },
    404: {
        "description": "Not Found",
        "content": {"application/json": {"example": {"detail": "menu not found"}}},
    },
}

get_menus_schema = {
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "empty": {"summary": "Пустой список меню", "value": []},
                    "full": {
                        "summary": "В списке содержатся записи",
                        "value": [
                            {
                                "id": uuid.uuid4(),
                                "title": "Меню 1",
                                "description": "Описание меню 1",
                                "submenus_count": random.randint(0, 10),
                                "dishes_count": random.randint(0, 10),
                            },
                            {
                                "id": uuid.uuid4(),
                                "title": "Меню 2",
                                "description": "Описание меню 2",
                                "submenus_count": random.randint(0, 10),
                                "dishes_count": random.randint(0, 10),
                            },
                            {
                                "id": uuid.uuid4(),
                                "title": "Меню 3",
                                "description": "Описание меню 3",
                                "submenus_count": random.randint(0, 10),
                                "dishes_count": random.randint(0, 10),
                            },
                        ],
                    },
                }
            }
        },
    }
}
