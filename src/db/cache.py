from abc import ABC, abstractmethod
from typing import Any


class AbstractCache(ABC):
    def __init__(self, cache_instance):
        self.cache = cache_instance

    @abstractmethod
    async def get(self, key: str) -> None:
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, expire: int = 0,) -> None:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        pass


cache: AbstractCache | None = None


async def get_cache() -> AbstractCache | None:
    return cache
