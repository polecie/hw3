from typing import NoReturn, Optional, Union

from src.core import config
from src.db.cache import AbstractCache


class CacheRedis(AbstractCache):
    async def get(self, key: str) -> Optional[dict]:
        """

        :param key:
        :return:
        """
        return self.cache.get(name=key)

    async def set(
        self,
        key: str,
        value: Union[bytes, str],
        expire: int = config.cache_expire_in_seconds,
    ):
        """

        :param key:
        :param value:
        :param expire:
        :return:
        """
        await self.cache.set(name=key, value=value, ex=expire)

    async def close(self) -> NoReturn:
        """

        :return:
        """
        await self.cache.close()

    async def delete(self, key: str):
        """

        :param key:
        :return:
        """
        await self.cache.delete(key)
