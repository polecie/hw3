from typing import NoReturn, Optional, Union

from src.core import config
from src.db.cache import AbstractCache


class CacheRedis(AbstractCache):
    async def get(self, key: str) -> Optional[dict]:
        """
        Получает значение по ключу.
        :param key: Ключ.
        """
        return await self.cache.get(name=key)

    async def set(
        self,
        key: str,
        value: Union[bytes, str, bytearray],
        expire: int = config.cache_expire_in_seconds,
    ):
        """
        Устанавливает значение по ключу и время его истечения.
        :param key: Ключ.
        :param value: Значение.
        :param expire: Время истечения в секундах.
        """
        await self.cache.set(name=key, value=value, ex=expire)

    async def close(self) -> NoReturn:
        """
        Закрывает соединение.
        """
        await self.cache.close()

    async def delete(self, key: str):
        """
        Удаляет значение по ключу.
        :param key: Ключ.
        """
        await self.cache.delete(key)

    async def flushall(self):
        """
        Удаляет все ключи.
        """
        keys = await self.cache.keys("*")
        if keys:
            await self.cache.delete(*keys)
