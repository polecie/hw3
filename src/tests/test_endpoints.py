import uuid

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio
uid = uuid.uuid4()


async def test_get_menus(client: AsyncClient):
    response = await client.get("api/v1/menus/")
    assert response.status_code == 200


async def test_get_menu_by_id(client: AsyncClient):
    response = await client.get(f"api/v1/menus/{uid}")
    assert response.status_code == 404
    assert response.json() == {"detail": "menu not found"}


async def test_delete_menu(client: AsyncClient):
    response = await client.delete(f"api/v1/menus/{uid}")
    assert response.status_code == 404
    assert response.json() == {"detail": "menu not found"}


async def test_patch_menu(client: AsyncClient):
    response = await client.delete(f"api/v1/menus/{uid}")
    assert response.status_code == 404
    assert response.json() == {"detail": "menu not found"}


async def test_get_submenu(client: AsyncClient):
    response = await client.get(f"api/v1/menus/{uid}/submenus")
    assert response.status_code == 200


async def test_get_submenu_by_id(client: AsyncClient):
    response = await client.get(f"api/v1/menus/{uid}/submenus/{uid}")
    assert response.status_code == 404
    assert response.json() == {"detail": "submenu not found"}


async def test_delete_submenu(client: AsyncClient):
    response = await client.delete(f"api/v1/menus/{uid}/submenus/{uid}")
    assert response.status_code == 404
    assert response.json() == {"detail": "submenu not found"}


async def test_patch_submenu(client: AsyncClient):
    response = await client.delete(f"api/v1/menus/{uid}/submenus/{uid}")
    assert response.status_code == 404
    assert response.json() == {"detail": "submenu not found"}


async def test_get_dish(client: AsyncClient):
    response = await client.get(f"api/v1/menus/{uid}/submenus/{uid}/dishes")
    assert response.status_code == 200


async def test_get_dish_by_id(client: AsyncClient):
    response = await client.get(f"api/v1/menus/{uid}/submenus/{uid}/dishes/{uid}")
    assert response.status_code == 404
    assert response.json() == {"detail": "dish not found"}


async def test_delete_dish(client: AsyncClient):
    response = await client.delete(f"api/v1/menus/{uid}/submenus/{uid}/dishes/{uid}")
    assert response.status_code == 404
    assert response.json() == {"detail": "dish not found"}


async def test_patch_dish(client: AsyncClient):
    response = await client.delete(f"api/v1/menus/{uid}/submenus/{uid}/dishes/{uid}")
    assert response.status_code == 404
    assert response.json() == {"detail": "dish not found"}
