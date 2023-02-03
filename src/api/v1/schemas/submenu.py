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
                                "id": "9202923d-afd2-4b4d-acb9-7d4c4f9bcc3a",
                                "title": "Подменю 1",
                                "description": "Описание подменю 1",
                                "dishes_count": 1,
                            },
                            {
                                "id": "779254bb-f0bd-4899-804e-0cb925d88621",
                                "title": "Подменю 2",
                                "description": "Описание подменю 2",
                                "dishes_count": 0,
                            },
                            {
                                "id": "781f9966-587a-49ed-a095-d10f5fe6ecf6",
                                "title": "Подменю 3",
                                "description": "Описание подменю 3",
                                "dishes_count": 9,
                            },
                        ],
                    },
                }
            }
        },
    }
}
