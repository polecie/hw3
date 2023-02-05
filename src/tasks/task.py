import json

from .utils import add_menus_to_sheet
from .worker import celery


@celery.task
def save_menu(menus) -> str:
    """Задача celery - сохранение меню в excel-файл."""
    menus = json.loads(menus)
    path: str = add_menus_to_sheet(menus)
    return path
