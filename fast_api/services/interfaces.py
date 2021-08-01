from abc import ABC, abstractmethod
from typing import Any, List, Optional


class GetListAndEntityService(ABC):
    @abstractmethod
    async def get_items_list(self, params: Any) -> Optional[List[Any]]:
        pass

    @abstractmethod
    async def get_by_id(self, item_id: str) -> Optional[Any]:
        pass


class AsyncCacheStorage(ABC):
    @abstractmethod
    async def get(self, key: str, **kwargs):
        pass

    @abstractmethod
    async def set(self, key: str, value: str, expire: int, **kwargs):
        pass


class AsyncFulltextDB(ABC):
    @abstractmethod
    async def get(self, index: Any, id: Any, **kwargs):
        pass

    @abstractmethod
    async def search(
        self, index: Any, body: Any, size: int, from_: int, sort: str, **kwargs
    ):
        pass
