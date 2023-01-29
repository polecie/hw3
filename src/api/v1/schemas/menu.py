from src.api.v1.schemas.base import BaseMenu, BaseSchema


class MenuBase(BaseSchema):
    """Базовая схема меню."""


class MenuSchema(MenuBase):
    """Схема меню."""

    class Config:
        """Пример схемы меню для документации."""

        schema_extra = {
            "example": {
                "title": "Меню",
                "description": "Описание меню",
            }
        }


class MenuResponse(BaseMenu):
    """Схема меню для ответа."""

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


class MenuCreate(MenuBase):
    class Config:
        schema_extra = {
            "examples": {
                "valid": {
                    "summary": "Верный формат запроса",
                    "description": "Ожидаемый формат данных для успешного ответа",
                    "value": {
                        "title": "My new menu",
                        "description": "Super cool menu for my restaurant",
                    },
                },
                "invalid": {
                    "summary": "Неверный формат запроса",
                    "description": "Невалидные данные, которые приведут к ошибке валидации",
                    "value": {
                        "name": "",
                        "description": "My new menu description",
                    },
                },
            }
        }


class MenuUpdate(MenuBase):
    class Config:
        schema_extra = {
            "examples": {
                "valid": {
                    "summary": "Верный формат запроса",
                    "description": "Ожидаемый формат данных для успешного ответа",
                    "value": {
                        "title": "My updated menu",
                        "description": "My updated cool menu",
                    },
                },
                "invalid": {
                    "summary": "Неверный формат запроса",
                    "description": "Невалидные данные, которые приведут к ошибке валидации",
                    "value": {
                        "title": "F",
                        "description": "F",
                    },
                },
            }
        }
