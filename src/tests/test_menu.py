import dataclasses
import random
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.models import Menu as menu_m

pytestmark = pytest.mark.asyncio


@dataclasses.dataclass
class Menu:
    menu: int = random.randint(0, 9)
    menu_id: str = ""
    title: str = "My menu title"
    description: str = "My menu description"
    submenus_count: int = 1
    dishes_count: int = 1
    message: str = "The menu has been deleted"


async def test_get_menu(client: AsyncClient):
    response = await client.get("api/v1/menus/")
    data = response.json()
    menu = Menu.menu
    assert "title" in data[menu]
    assert "dishes_count" in data[menu]
    assert data[menu]["dishes_count"] == Menu.dishes_count
    assert data[menu]["submenus_count"] == Menu.submenus_count
    assert "description" in data[menu]
    Menu.menu_id = data[menu]["id"]
    Menu.title = data[menu]["title"]
    Menu.description = data[menu]["description"]


async def test_get_menu_by_id(client: AsyncClient, session: AsyncSession):
    response = await client.get(f"api/v1/menus/{Menu.menu_id}")
    data = response.json()
    assert response.status_code == 200
    statement = select(menu_m).where(menu_m.id == Menu.menu_id)
    menu = (await session.execute(statement)).scalars().first()
    assert str(menu.id) == data["id"]
    assert menu.title == data["title"]
    assert menu.description == data["description"]


async def test_update_menu(client: AsyncClient, session: AsyncSession):
    Menu.title = "My updated menu 1"
    Menu.description = "My updated menu description 1"
    response = await client.patch(f"api/v1/menus/{Menu.menu_id}",
                                  json={"title": Menu.title, "description": Menu.description})
    data = response.json()
    assert response.status_code == 200
    assert "id" in data


async def test_updated_menu(client: AsyncClient, session: AsyncSession):
    response = await client.get(f"api/v1/menus/{Menu.menu_id}")
    data = response.json()
    assert response.status_code == 200

    statement = select(menu_m).where(menu_m.id == Menu.menu_id)
    menu = (await session.execute(statement)).scalars().first()
    assert menu.title == data["title"]
    assert Menu.title == data["title"]
    assert menu.description == data["description"]


async def test_create_menu(client: AsyncClient):
    response = await client.post(
        "api/v1/menus/",
        json={"title": Menu.title, "description": Menu.description})
    data = response.json()
    assert response.status_code == 201
    assert data["title"] == Menu.title
    assert data["description"] == Menu.description
    assert "id" in data
    Menu.menu_id = data["id"]


async def test_get_created_menu(client: AsyncClient, session: AsyncSession):
    response = await client.get(f"api/v1/menus/{Menu.menu_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == Menu.title
    assert data["description"] == Menu.description


async def test_delete_menu(client: AsyncClient, session: AsyncSession):
    response = await client.get("api/v1/menus/")
    assert response.status_code == 200
    data = response.json()
    menu = Menu.menu
    uid = data[menu]["id"]
    Menu.menu_id = uid
    response = await client.get(f"api/v1/menus/{uid}")
    assert response.status_code == 200
    response = await client.delete(f"api/v1/menus/{uid}")
    assert response.status_code == 200
    data = response.json()
    assert data == {'status': True, 'message': Menu.message}


async def test_check_deleted_menu(client: AsyncClient):
    response = await client.get(f"api/v1/menus/{Menu.menu_id}")
    assert response.status_code == 404
    data = response.json()
    assert data == {"detail": "menu not found"}