import uuid

from fastapi import APIRouter, Body, Depends

from src.api.v1.schemas.submenu import (
    SubmenuCreate,
    SubmenuResponse,
    SubmenuUpdate,
    delete_submenu_schema,
    get_submenus_schema,
    submenu_not_found_schema,
)
from src.services.submenu import SubmenuService, get_submenu_service

router = APIRouter()


@router.get(
    path="/{menu_id}/submenus",
    summary="Просмотр списка подменю",
    status_code=200,
    response_model=list[SubmenuResponse],
    responses=get_submenus_schema,
)
async def get_submenus(
    menu_id: uuid.UUID,
    submenu_service: SubmenuService = Depends(get_submenu_service),
) -> list[SubmenuResponse]:
    """Возвращает список всех подменю, связанных с меню.
    """
    submenus: list[SubmenuResponse] = await submenu_service.get_submenus(menu_id)
    return submenus


@router.get(
    path="/{menu_id}/submenus/{submenu_id}",
    summary="Просмотр определенного подменю",
    status_code=200,
    response_model=SubmenuResponse,
    responses=submenu_not_found_schema,
)
async def get_submenu(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    submenu_service: SubmenuService = Depends(get_submenu_service),
) -> SubmenuResponse:
    """Возвращает подменю по его **id** в меню.
    """
    submenu: SubmenuResponse = await submenu_service.get_submenu(submenu_id, menu_id)
    return submenu


@router.post(
    path="/{menu_id}/submenus",
    summary="Создать подменю",
    status_code=201,
    response_model=SubmenuResponse,
)
async def create_submenu(
    menu_id: uuid.UUID,
    submenu_content: SubmenuCreate = Body(None, examples=SubmenuCreate.Config.schema_extra["examples"]),
    submenu_service: SubmenuService = Depends(get_submenu_service),
) -> SubmenuResponse:
    """Создает новое подменю в меню. Принимает аргументы для создания подменю - **title** (название подменю), **description** (описание подменю).
    """
    submenu: SubmenuResponse = await submenu_service.create_submenu(submenu_content, menu_id)
    return submenu


@router.patch(
    path="/{menu_id}/submenus/{submenu_id}",
    summary="Обновить подменю",
    status_code=200,
    response_model=SubmenuResponse,
    responses=submenu_not_found_schema,
)
async def patch_submenu(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    submenu_content: SubmenuUpdate = Body(None, examples=SubmenuUpdate.Config.schema_extra["examples"]),
    submenu_service: SubmenuService = Depends(get_submenu_service),
) -> SubmenuResponse:
    """Изменяет подменю в меню. В качестве аргументов для изменения принимает **title** (название подменю), **description** (описание подменю).
    """
    submenu: SubmenuResponse = await submenu_service.update_submenu(submenu_id, submenu_content, menu_id)
    return submenu


@router.delete(
    path="/{menu_id}/submenus/{submenu_id}",
    summary="Удалить подменю",
    status_code=200,
    response_model=dict,
    responses=delete_submenu_schema,
)
async def delete_submenu(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    submenu_service: SubmenuService = Depends(get_submenu_service),
) -> dict:
    """Каскадно удаляет подменю в меню по его **id**.
    """
    submenu: dict = await submenu_service.delete_submenu(submenu_id, menu_id)
    return submenu
