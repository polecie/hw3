import dataclasses
import random
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.models import Submenu as submenu_m

pytestmark = pytest.mark.asyncio


@dataclasses.dataclass
class Submenu:
    menu_id: str = ""
    menus: int = random.randint(0, 8)
    submenu_id: str = ""
    title: str = "My submenu title"
    description: str = "My submenu description"
    dishes_count: int = 1
    message: str = "The submenu has been deleted"


async def test_get_menu(client: AsyncClient):
    response = await client.get("api/v1/menus/")
    data = response.json()
    menus = Submenu.menus
    Submenu.menu_id = data[menus]["id"]
    assert response.status_code == 200
    response = await client.get(f"api/v1/menus/{Submenu.menu_id}/submenus")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    Submenu.submenu_id = data[0]["id"]
    Submenu.title = data[0]["title"]
    Submenu.description = data[0]["description"]


async def test_get_submenu_by_id(client: AsyncClient, session: AsyncSession):
    response = await client.get(f"api/v1/menus/{Submenu.menu_id}/submenus/{Submenu.submenu_id}")
    data = response.json()
    assert response.status_code == 200
    statement = select(submenu_m).where(submenu_m.id == Submenu.submenu_id)
    submenu = (await session.execute(statement)).scalars().first()
    assert str(submenu.id) == data["id"]
    assert submenu.title == data["title"]
    assert submenu.description == data["description"]


async def test_update_submenu(client: AsyncClient, session: AsyncSession):
    Submenu.title = "My updated submenu 1"
    Submenu.description = "My updated submenu description 1"
    response = await client.patch(f"api/v1/menus/{Submenu.menu_id}/submenus/{Submenu.submenu_id}",
                                  json={"title": Submenu.title, "description": Submenu.description})
    data = response.json()
    assert response.status_code == 200
    assert "id" in data


async def test_updated_submenu(client: AsyncClient, session: AsyncSession):
    response = await client.get(f"api/v1/menus/{Submenu.menu_id}/submenus/{Submenu.submenu_id}")
    data = response.json()
    assert response.status_code == 200
    statement = select(submenu_m).where(submenu_m.id == Submenu.submenu_id).where(submenu_m.menu_id == Submenu.menu_id)
    submenu = (await session.execute(statement)).scalars().first()
    assert submenu.title == data["title"]
    assert Submenu.title == data["title"]
    assert submenu.description == data["description"]


async def test_create_submenu(client: AsyncClient):
    response = await client.post(
        f"api/v1/menus/{Submenu.menu_id}/submenus",
        json={"title": Submenu.title, "description": Submenu.description})
    data = response.json()
    assert response.status_code == 201
    assert data["title"] == Submenu.title
    assert data["description"] == Submenu.description
    assert "id" in data
    Submenu.submenu_id = data["id"]


async def test_get_created_submenu(client: AsyncClient, session: AsyncSession):
    response = await client.get(f"api/v1/menus/{Submenu.menu_id}/submenus/{Submenu.submenu_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == Submenu.title
    assert data["description"] == Submenu.description


async def test_delete_submenu(client: AsyncClient, session: AsyncSession):
    response = await client.get(f"api/v1/menus/")
    assert response.status_code == 200
    data = response.json()
    menu = Submenu.menus
    uid = data[menu]["id"]
    Submenu.menu_id = uid
    response = await client.get(f"api/v1/menus/{Submenu.menu_id}/submenus")
    assert response.status_code == 200
    data = response.json()
    Submenu.submenu_id = data[1]["id"]
    response = await client.delete(f"api/v1/menus/{uid}/submenus/{Submenu.submenu_id}")
    assert response.status_code == 200
    data = response.json()
    assert data == {'status': True, 'message': Submenu.message}


async def test_check_deleted_submenu(client: AsyncClient):
    response = await client.get(f"api/v1/menus/{Submenu.menu_id}/submenus/{Submenu.submenu_id}")
    assert response.status_code == 404
    data = response.json()
    assert data == {"detail": "submenu not found"}