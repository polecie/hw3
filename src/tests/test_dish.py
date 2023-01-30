import dataclasses
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.models import Dish as dish_m

pytestmark = pytest.mark.asyncio


@dataclasses.dataclass
class Dish:
    menu_id: str = ""
    dish_id: str = ""
    submenu_id: str = ""
    title: str = "My dish title"
    description: str = "My dish description"
    price: float = 234.345
    message: str = "The dish has been deleted"


async def test_get_menu_and_submenu_ids(client: AsyncClient, session: AsyncSession):
    response_menu = await client.get(f"api/v1/menus/")
    assert response_menu.status_code == 200
    menus = response_menu.json()
    Dish.menu_id = menus[3]["id"]
    response_submenu = await client.get(f"api/v1/menus/{Dish.menu_id}/submenus")
    assert response_submenu.status_code == 200
    submenus = response_submenu.json()
    Dish.submenu_id = submenus[0]["id"]
    response_id = await client.get(f"api/v1/menus/{Dish.menu_id}/submenus/{Dish.submenu_id}")
    assert response_id.status_code == 200
    dish = response_id.json()
    Dish.dish_id = dish["id"]


async def test_get_dishes(client: AsyncClient, session: AsyncSession):
    response = await client.get(
        f"api/v1/menus/{Dish.menu_id}/submenus/{Dish.submenu_id}/dishes")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    Dish.dish_id = data[0]["id"]


async def test_get_dish_by_id(client: AsyncClient, session: AsyncSession):
    response = await client.get(
        f"api/v1/menus/{Dish.menu_id}/submenus/{Dish.submenu_id}/dishes/{Dish.dish_id}")
    assert response.status_code == 200
    data = response.json()
    statement = select(dish_m).where(dish_m.id == Dish.dish_id)
    dish = (await session.execute(statement)).scalars().first()
    assert str(dish.id) == data["id"]
    assert dish.title == data["title"]
    assert dish.description == data["description"]
    assert str(dish.submenu_id) == Dish.submenu_id


async def test_update_dish(client: AsyncClient, session: AsyncSession):
    Dish.title = "My updated dish 1"
    Dish.description = "My updated dish description 1"
    response = await client.patch(
        f"api/v1/menus/{Dish.menu_id}/submenus/{Dish.submenu_id}/dishes/{Dish.dish_id}",
        json={"title": Dish.title, "description": Dish.description, "price": Dish.price})
    data = response.json()
    assert response.status_code == 200
    assert "id" in data


async def test_updated_dish(client: AsyncClient, session: AsyncSession):
    response = await client.get(
        f"api/v1/menus/{Dish.menu_id}/submenus/{Dish.submenu_id}/dishes/{Dish.dish_id}")
    data = response.json()
    assert response.status_code == 200
    statement = select(dish_m).where(dish_m.id == Dish.dish_id).where(dish_m.submenu_id == Dish.submenu_id)
    dish = (await session.execute(statement)).scalars().first()
    assert dish.title == data["title"]
    assert Dish.title == data["title"]
    assert dish.description == data["description"]


async def test_create_dish(client: AsyncClient):
    response = await client.post(
        f"api/v1/menus/{Dish.menu_id}/submenus/{Dish.submenu_id}/dishes",
        json={"title": Dish.title, "description": Dish.description, "price": Dish.price})
    data = response.json()
    assert response.status_code == 201
    assert data["title"] == Dish.title
    assert data["description"] == Dish.description
    assert "id" in data
    Dish.dish_id = data["id"]


async def test_get_created_dish(client: AsyncClient, session: AsyncSession):
    response = await client.get(
        f"api/v1/menus/{Dish.menu_id}/submenus/{Dish.submenu_id}/dishes/{Dish.dish_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == Dish.title
    assert data["description"] == Dish.description


async def test_delete_dish(client: AsyncClient, session: AsyncSession):
    response = await client.delete(
        f"api/v1/menus/{Dish.menu_id}/submenus/{Dish.submenu_id}/dishes/{Dish.dish_id}")
    assert response.status_code == 200
    data = response.json()
    assert data == {'status': True, 'message': Dish.message}


async def test_check_deleted_dish(client: AsyncClient):
    response = await client.get(
        f"api/v1/menus/{Dish.menu_id}/submenus/{Dish.submenu_id}/dishes/{Dish.dish_id}")
    assert response.status_code == 404
    data = response.json()
    assert data == {"detail": "dish not found"}