from abc import ABC, abstractmethod


class AbstractCache(ABC):
    def __init__(self, cache_instance):
        self.cache = cache_instance

    @abstractmethod
    async def get(self, key: str):  # type: ignore
        raise NotImplementedError

    @abstractmethod
    async def set(self, key: str, value: bytes | str | bytearray, expire: int = 0):
        raise NotImplementedError

    @abstractmethod
    async def close(self):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, key: str):
        raise NotImplementedError

    async def flushall(self):
        raise NotImplementedError


cache: AbstractCache | None = None
report_cache: AbstractCache | None = None


async def get_cache() -> AbstractCache | None:
    """Функция необходима для внедрения зависимостей."""
    return cache


async def get_report_cache() -> AbstractCache | None:
    """Функция необходима для внедрения зависимостей."""
    return report_cache
