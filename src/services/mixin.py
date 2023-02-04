from dataclasses import dataclass

from src.db.cache import AbstractCache
from src.repositories.container import AbstractRepositoriesContainer


@dataclass
class ServiceMixin:
    cache: AbstractCache
    container: AbstractRepositoriesContainer


# @dataclass
# class Service:
#     container: AbstractRepositoriesContainer
