import uuid

from fastapi import APIRouter, Depends

from src.api.v1.schemas.submenu import SubmenuResponse, SubmenuSchema
from src.services.submenu import SubmenuService, get_submenu_service

router = APIRouter()


@router.get(
    path="/{menu_id}/submenus",
    summary="Просмотр списка подменю",
    tags=["submenu"],
    status_code=200,
    response_model=list[SubmenuResponse],
)
async def get_submenus(
    menu_id: uuid.UUID,
    submenu_service: SubmenuService = Depends(get_submenu_service),
) -> list[SubmenuResponse]:
    """Возвращает список всех подменю.

    :param menu_id: Идентификатор меню.
    :param submenu_service: Сервис для работы с логикой.
    """
    submenus: list[SubmenuResponse] = await submenu_service.get_submenus(
        menu_id
    )
    return submenus


@router.get(
    path="/{menu_id}/submenus/{submenu_id}",
    summary="Просмотр определенного подменю",
    tags=["submenu"],
    status_code=200,
    response_model=SubmenuResponse,
)
async def get_submenu(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    submenu_service: SubmenuService = Depends(get_submenu_service),
) -> SubmenuResponse:
    """Возвращает подменю по его `id`.

    :param menu_id: Идентификатор меню.
    :param submenu_id: Идентификатор подменю.
    :param submenu_service: Сервис для работы с логикой.
    """
    submenu: SubmenuResponse = await submenu_service.get_submenu(
        submenu_id, menu_id
    )
    return submenu


@router.post(
    path="/{menu_id}/submenus",
    summary="Создать подменю",
    tags=["submenu"],
    status_code=201,
    response_model=SubmenuResponse,
)
async def create_submenu(
    menu_id: uuid.UUID,
    submenu_content: SubmenuSchema,
    submenu_service: SubmenuService = Depends(get_submenu_service),
) -> SubmenuResponse:
    """Создает новое подменю.

    :param menu_id: Идентификатор меню.
    :param submenu_content: Поля для создания подменю.
    :param submenu_service: Сервис для работы с логикой.
    """
    submenu: SubmenuResponse = await submenu_service.create_submenu(
        submenu_content, menu_id
    )
    return submenu


@router.patch(
    path="/{menu_id}/submenus/{submenu_id}",
    summary="Обновить подменю",
    tags=["submenu"],
    status_code=200,
    response_model=SubmenuResponse,
)
async def patch_submenu(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    submenu_content: SubmenuSchema,
    submenu_service: SubmenuService = Depends(get_submenu_service),
) -> SubmenuResponse:
    """Изменияет подменю.

    :param menu_id: Идентификатор меню.
    :param submenu_id: Идентификатор подменю.
    :param submenu_content: Поля для обновления подменю.
    :param submenu_service: Сервис для работы с логикой.
    """
    submenu: SubmenuResponse = await submenu_service.update_submenu(
        submenu_id, submenu_content, menu_id
    )
    return submenu


@router.delete(
    path="/{menu_id}/submenus/{submenu_id}",
    summary="Удалить подменю",
    tags=["submenu"],
    status_code=200,
    response_model=dict,
)
async def delete_submenu(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    submenu_service: SubmenuService = Depends(get_submenu_service),
) -> dict:
    """Удаляет подменю.

    :param menu_id: Идентификатор подменю.
    :param submenu_id: Идентификатор подменю.
    :param submenu_service: Сервис для работы с логикой.
    """
    submenu: dict = await submenu_service.delete_submenu(submenu_id, menu_id)
    return submenu
