from abc import ABC, abstractmethod


class AbstractCache(ABC):
    def __init__(self, cache_instance):
        self.cache = cache_instance

    @abstractmethod
    async def get(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    async def set(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, *args, **kwargs) -> None:
        raise NotImplementedError

    async def flushall(self) -> None:
        raise NotImplementedError


cache: AbstractCache | None = None


async def get_cache() -> AbstractCache | None:
    """
    Функция необходима для внедрения зависимостей.
    """
    return cache
