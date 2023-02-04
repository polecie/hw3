import uuid

from fastapi import APIRouter, Body, Depends

from src.api.v1.schemas.menu import (
    MenuCreate,
    MenuResponse,
    MenuUpdate,
    delete_menu_schema,
    get_menus_schema,
    menu_not_found_schema,
)
from src.services.menu import MenuService, get_menu_service

router = APIRouter()


@router.get(
    path="/",
    summary="Просмотр списка меню",
    status_code=200,
    response_model=list[MenuResponse],
    responses=get_menus_schema,
)
async def get_menus(
    menu_service: MenuService = Depends(get_menu_service),
) -> list[MenuResponse]:
    """Возвращает список всех меню."""
    menus: list[MenuResponse] = await menu_service.get_menus()
    return menus


@router.get(
    path="/{menu_id}",
    summary="Просмотр определенного меню",
    status_code=200,
    response_model=MenuResponse,
    responses=menu_not_found_schema,
)
async def get_menu(menu_id: uuid.UUID, menu_service: MenuService = Depends(get_menu_service)) -> MenuResponse:
    """Возвращает меню по его **id**."""
    menu: MenuResponse = await menu_service.get_menu(menu_id)
    return menu


@router.post(
    path="/",
    summary="Создать меню",
    status_code=201,
    response_model=MenuResponse,
)
async def create_menu(
    menu_content: MenuCreate = Body(None, examples=MenuCreate.Config.schema_extra["examples"]),
    menu_service: MenuService = Depends(get_menu_service),
) -> MenuResponse:
    """Создает новое меню. В качестве параметров принимает **title** - название меню, **description** - описание меню.
    """
    menu: MenuResponse = await menu_service.create_menu(menu_content)
    return menu


@router.patch(
    path="/{menu_id}",
    summary="Обновить меню",
    status_code=200,
    response_model=MenuResponse,
    responses=menu_not_found_schema,
)
async def patch_menu(
    menu_id: uuid.UUID,
    menu_content: MenuUpdate = Body(None, examples=MenuUpdate.Config.schema_extra["examples"]),
    menu_service: MenuService = Depends(get_menu_service),
) -> MenuResponse:
    """Обновляет меню. Для обновления меню принимает аргументы - **title** (название меню), **description** (описание меню).
    """
    menu: MenuResponse = await menu_service.update_menu(menu_id, menu_content)
    return menu


@router.delete(
    path="/{menu_id}",
    summary="Удалить меню",
    status_code=200,
    response_model=dict,
    responses=delete_menu_schema,
)
async def delete_menu(menu_id: uuid.UUID, menu_service: MenuService = Depends(get_menu_service)) -> dict:
    """Каскадно удаляет меню по его **id**.
    """
    menu: dict = await menu_service.delete_menu(menu_id)
    return menu
