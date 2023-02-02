from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.cache import AbstractCache
from src.repositories.container import AbstractRepositoriesContainer


@dataclass
class ServiceMixin:
    cache: AbstractCache
    container: AbstractRepositoriesContainer


@dataclass
class Service:
    session: AsyncSession
