from src.api.v1.schemas.base import BaseSchema, BaseSubmenu


class SubmenuBase(BaseSchema):
    """Базовая схема подменю."""


class SubmenuSchema(SubmenuBase):
    """Схема подменю."""

    class Config:
        """Пример схемы для документации."""

        schema_extra = {
            "example": {
                "title": "Подменю",
                "description": "Описание подменю",
            }
        }


class SubmenuResponse(BaseSubmenu):
    """Схема подменю для ответа."""

    class Config:
        """Пример схемы подменю для документации."""

        schema_extra = {
            "example": {
                "id": "f2f48e47-49dd-45a9-9f8d-a04af3b0cc19",
                "title": "Подменю",
                "description": "Описание подменю",
                "dishes_count": 5,
            }
        }

        orm_mode = True


class SubmenuCreate(SubmenuBase):
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


class SubmenuUpdate(SubmenuBase):
    class Config:
        schema_extra = {
            "examples": {
                "valid": {
                    "summary": "Верный формат запроса",
                    "description": "Ожидаемый формат данных для успешного ответа",
                    "value": {
                        "title": "My updated submenu",
                        "description": "My updated cool submenu",
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
