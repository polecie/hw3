from dataclasses import dataclass

from src.db.cache import AbstractCache
from src.repositories.container import AbstractRepositoriesContainer


@dataclass
class ServiceMixin:
    cache: AbstractCache
    container: AbstractRepositoriesContainer

    # def __post_init__(self):
    #     if self.cache is None:
    #         self.cache =
