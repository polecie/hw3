from abc import ABC, abstractmethod
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

__all__ = ("AbstractRepository",)


@dataclass
class AbstractRepository(ABC):
    session: AsyncSession

    @abstractmethod
    async def get(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def list(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def add(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def update(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, *args, **kwargs):
        raise NotImplementedError
