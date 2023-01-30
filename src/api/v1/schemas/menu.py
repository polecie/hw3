from src.api.v1.schemas.base import BaseMenu, BaseSchema


class MenuSchema(BaseSchema):
    """Схема меню для обновления данных."""


class MenuResponse(BaseMenu):
    """Схема меню для успешного ответа."""

    class Config:
        """Пример схемы меню для документации."""

        schema_extra = {
            "example": {
                "id": "9202923d-afd2-4b4d-acb9-7d4c4f9bcc3a",
                "title": "Меню",
                "description": "Описание меню",
                "submenus_count": 3,
                "dishes_count": 0,
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
