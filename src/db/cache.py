from abc import ABC, abstractmethod
from typing import Any


class AbstractCache(ABC):
    def __init__(self, cache_instance):
        self.cache = cache_instance

    @abstractmethod
    async def get(self, key: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def set(
        self,
        key: str,
        value: Any,
        expire: int = 0,
    ) -> None:
        # str, bytes or bytearray
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, key: str) -> None:
        raise NotImplementedError

    async def flushall(self) -> None:
        raise NotImplementedError


cache: AbstractCache | None = None


async def get_cache() -> AbstractCache | None:
    return cache
