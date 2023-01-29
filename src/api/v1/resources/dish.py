import uuid

from fastapi import APIRouter, Depends

from src.api.v1.schemas.dish import DishResponse, DishSchema
from src.services.dish import DishService, get_dish_service

router = APIRouter()


@router.get(
    path="/{menu_id}/submenus/{submenu_id}/dishes",
    summary="Просмотр списка блюд",
    tags=["dish"],
    status_code=200,
    response_model=list[DishResponse],
)
async def get_dishes(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    dish_service: DishService = Depends(get_dish_service),
) -> list[DishResponse]:
    """
    Получить список всех блюд.
    :param menu_id: Идентификатор меню.
    :param submenu_id: Идентификатор подменю.
    :param dish_service: Сервис для работы с логикой.
    """
    dishes: list[DishResponse] = await dish_service.get_dishes(
        menu_id, submenu_id
    )
    return dishes


@router.get(
    path="/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    summary="Просмотр определенного блюда",
    tags=["dish"],
    status_code=200,
    response_model=DishResponse,
)
async def get_dish(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    dish_id: uuid.UUID,
    dish_service: DishService = Depends(get_dish_service),
) -> DishResponse:
    """
    Просмотр определенного блюда по его `id`.
    :param menu_id: Идентификатор меню.
    :param submenu_id: Идентификатор подменю.
    :param dish_id: Идентификатор блюда.
    :param dish_service: Сервис для работы с логикой.
    """
    dish: DishResponse = await dish_service.get_dish(
        menu_id, submenu_id, dish_id
    )
    return dish


@router.post(
    path="/{menu_id}/submenus/{submenu_id}/dishes",
    summary="Создать блюдо",
    tags=["dish"],
    status_code=201,
    response_model=DishResponse,
)
async def create_dish(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    dish_content: DishSchema,
    dish_service: DishService = Depends(get_dish_service),
) -> DishResponse:
    """
    Создать новое блюдо.
    :param menu_id: Идентификатор меню.
    :param submenu_id: Идентификатор подменю.
    :param dish_content: Поля для создания записи о блюде.
    :param dish_service: Сервис для работы с логикой.
    """
    dish: DishResponse = await dish_service.create_dish(
        menu_id, submenu_id, dish_content
    )
    return dish


@router.patch(
    path="/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    summary="Обновить блюдо",
    tags=["dish"],
    status_code=200,
    response_model=DishResponse,
)
async def patch_dish(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    dish_id: uuid.UUID,
    dish_content: DishSchema,
    dish_service: DishService = Depends(get_dish_service),
) -> DishResponse:
    """
    Обновить блюдо.
    :param menu_id: Идентификатор меню.
    :param submenu_id: Идентификатор подменю.
    :param dish_id: Идентификатор блюда.
    :param dish_content: Поля для обновления блюда.
    :param dish_service: Сервис для работы с логикой.
    """
    dish: DishResponse = await dish_service.update_dish(
        menu_id, submenu_id, dish_id, dish_content
    )
    return dish


@router.delete(
    path="/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    summary="Удалить блюдо",
    tags=["dish"],
    status_code=200,
    response_model=dict,
)
async def delete_dish(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    dish_id: uuid.UUID,
    dish_service: DishService = Depends(get_dish_service),
) -> dict:
    """
    Удалить блюдо.
    :param menu_id: Идентификатор меню.
    :param submenu_id: Идентификатор подменю.
    :param dish_id: Идентификатор блюда.
    :param dish_service: Сервис для работы с логикой.
    """
    dish: dict = await dish_service.delete_dish(menu_id, submenu_id, dish_id)
    return dish
