import uuid

from fastapi import APIRouter, Body, Depends

from src.api.v1.schemas.dish import (
    DishCreate,
    DishResponse,
    DishUpdate,
    delete_dish_schema,
    dish_not_found_schema,
    get_dishes_schema,
)
from src.services.dish import DishService, get_dish_service

router = APIRouter()


@router.get(
    path="/{menu_id}/submenus/{submenu_id}/dishes",
    summary="Просмотр списка блюд",
    status_code=200,
    response_model=list[DishResponse],
    responses=get_dishes_schema,
)
async def get_dishes(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    dish_service: DishService = Depends(get_dish_service),
) -> list[DishResponse]:
    """Возвращает список всех блюд в подменю конкретного меню.
    """
    dishes: list[DishResponse] = await dish_service.get_dishes(menu_id, submenu_id)
    return dishes


@router.get(
    path="/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    summary="Просмотр определенного блюда",
    status_code=200,
    response_model=DishResponse,
    responses=dish_not_found_schema,
)
async def get_dish(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    dish_id: uuid.UUID,
    dish_service: DishService = Depends(get_dish_service),
) -> DishResponse:
    """Возвращает определенное блюдо по его **id** из списка блюд, связанных с конкретными подменю и меню.
    """
    dish: DishResponse = await dish_service.get_dish(menu_id, submenu_id, dish_id)
    return dish


@router.post(
    path="/{menu_id}/submenus/{submenu_id}/dishes",
    summary="Создать блюдо",
    status_code=201,
    response_model=DishResponse,
)
async def create_dish(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    dish_content: DishCreate = Body(None, examples=DishCreate.Config.schema_extra["examples"]),
    dish_service: DishService = Depends(get_dish_service),
) -> DishResponse:
    """Создает новое блюдо в подменю конкретного меню. В качестве аргументов принимает
    **title** (название блюда), **description** (описание блюда) и **price** (цена блюда).
    """
    dish: DishResponse = await dish_service.create_dish(menu_id, submenu_id, dish_content)
    return dish


@router.patch(
    path="/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    summary="Обновить блюдо",
    status_code=200,
    response_model=DishResponse,
    responses=dish_not_found_schema,
)
async def patch_dish(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    dish_id: uuid.UUID,
    dish_content: DishUpdate = Body(None, examples=DishUpdate.Config.schema_extra["examples"]),
    dish_service: DishService = Depends(get_dish_service),
) -> DishResponse:
    """Обновляет блюдо в подменю конкретного меню. В качестве аргументов для обновления полей принимает
    **title** (название блюда), **description** (описание блюда) и **price** (цена блюда).
    """
    dish: DishResponse = await dish_service.update_dish(menu_id, submenu_id, dish_id, dish_content)
    return dish


@router.delete(
    path="/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    summary="Удалить блюдо",
    status_code=200,
    response_model=dict,
    responses=delete_dish_schema,
)
async def delete_dish(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    dish_id: uuid.UUID,
    dish_service: DishService = Depends(get_dish_service),
) -> dict:
    """Удаляет блюдо из подменю конкретного меню по его **id**.
    """
    dish: dict = await dish_service.delete_dish(menu_id, submenu_id, dish_id)
    return dish
