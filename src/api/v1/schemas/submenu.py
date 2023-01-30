from src.api.v1.schemas.base import BaseSchema, BaseSubmenu


class SubmenuSchema(BaseSchema):
    """Схема подменю для обновления данных."""


class SubmenuResponse(BaseSubmenu):
    """Схема подменю для успешного ответа."""

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
