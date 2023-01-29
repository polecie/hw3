import uuid

from fastapi import APIRouter, Depends

from src.api.v1.schemas.menu import MenuResponse, MenuSchema
from src.services.menu import MenuService, get_menu_service

router = APIRouter()


@router.get(
    path="/",
    summary="Просмотр списка меню",
    tags=["menu"],
    status_code=200,
    response_model=list[MenuResponse],
)
async def get_menus(
    menu_service: MenuService = Depends(get_menu_service),
) -> list[MenuResponse]:
    """
    Возвращает список всех меню.
    :param menu_service: Сервис для работы с логикой.
    """
    menus: list[MenuResponse] = await menu_service.get_menus()
    return menus


@router.get(
    path="/{menu_id}",
    summary="Просмотр определенного меню",
    tags=["menu"],
    status_code=200,
    response_model=MenuResponse,
)
async def get_menu(
    menu_id: uuid.UUID, menu_service: MenuService = Depends(get_menu_service)
) -> MenuResponse:
    """
    Возвращает меню по его `id`.
    :param menu_id: Идентификатор подменю.
    :param menu_service: Сервис для работы с логикой.
    """
    menu: MenuResponse = await menu_service.get_menu(menu_id)
    return menu


@router.post(
    path="/",
    summary="Создать меню",
    tags=["menu"],
    status_code=201,
    response_model=MenuResponse,
)
async def create_menu(
    menu_content: MenuSchema,
    menu_service: MenuService = Depends(get_menu_service),
) -> MenuResponse:
    """
    Создает новое меню,
    :param menu_content: Поля для создания меню.
    :param menu_service: Сервис для работы с логикой.
    """
    menu: MenuResponse = await menu_service.create_menu(menu_content)
    return menu


@router.patch(
    path="/{menu_id}",
    summary="Обновить меню",
    tags=["menu"],
    status_code=200,
    response_model=MenuResponse,
)
async def patch_menu(
    menu_id: uuid.UUID,
    menu_content: MenuSchema,
    menu_service: MenuService = Depends(get_menu_service),
) -> MenuResponse:
    """
    Изменяет меню.
    :param menu_id: Идентификатор меню.
    :param menu_content: Поля для обновления меню.
    :param menu_service: Сервис для работы с логикой.
    """
    menu: MenuResponse = await menu_service.update_menu(menu_id, menu_content)
    return menu


@router.delete(
    path="/{menu_id}",
    summary="Удалить меню",
    tags=["menu"],
    status_code=200,
    response_model=dict,
)
async def delete_menu(
    menu_id: uuid.UUID, menu_service: MenuService = Depends(get_menu_service)
) -> dict:
    """
    Удаляет меню по его `id`.
    :param menu_id: Идентификатор меню.
    :param menu_service: Сервис для работы с логикой.
    """
    menu: dict = await menu_service.delete_menu(menu_id)
    return menu
