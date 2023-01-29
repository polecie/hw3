import uuid

from fastapi import APIRouter, Depends

from src.api.v1.schemas.menu import MenuSchema, MenuResponse
from src.services.menu import get_menu_service, MenuService

router = APIRouter()


@router.get(
    path="/",
    summary="Просмотр списка меню",
    tags=["menu"],
    status_code=200,
    response_model=list[MenuResponse])
async def get_menus(
        menu_service: MenuService = Depends(get_menu_service)
) -> list[MenuResponse]:
    """
    Список всех меню
    :param menu_service:
    :return:
    """
    menus: list[MenuResponse] = await menu_service.get_menus()
    return menus


@router.get(
    path="/{menu_id}",
    summary="Просмотр определенного меню",
    tags=["menu"],
    status_code=200,
    response_model=MenuResponse)
async def get_menu(
        menu_id: uuid.UUID,
        menu_service: MenuService = Depends(get_menu_service)
) -> MenuResponse:
    """
    Просмотреть меню по его id
    :param menu_id:
    :param menu_service:
    :return:
    """
    menu: MenuResponse = await menu_service.get_menu(menu_id)
    return menu


@router.post(
    path="/",
    summary="Создать меню",
    tags=["menu"],
    status_code=201,
    response_model=MenuResponse)
async def create_menu(
        menu_content: MenuSchema,
        menu_service: MenuService = Depends(get_menu_service)
) -> MenuResponse:
    """
    Создать меню
    :param menu_content:
    :param menu_service:
    :return:
    """
    menu: MenuResponse = await menu_service.create_menu(menu_content)
    return menu


@router.patch(
    path="/{menu_id}",
    summary="Обновить меню",
    tags=["menu"],
    status_code=200,
    response_model=MenuResponse)
async def patch_menu(
        menu_id: uuid.UUID,
        menu_content: MenuSchema,
        menu_service: MenuService = Depends(get_menu_service)
) -> MenuResponse:
    """
    Изменить меню
    :param menu_id:
    :param menu_content:
    :param menu_service:
    :return:
    """
    menu: MenuResponse = await menu_service.update_menu(menu_id, menu_content)
    return menu


@router.delete(
    path="/{menu_id}",
    summary="Удалить меню",
    tags=["menu"],
    status_code=200,
    response_model=dict)
async def delete_menu(
        menu_id: uuid.UUID,
        menu_service: MenuService = Depends(get_menu_service)
) -> dict:
    """
    Удалить меню по его id
    :param menu_id:
    :param menu_service:
    :return:
    """
    menu: dict = await menu_service.delete_menu(menu_id)
    return menu
