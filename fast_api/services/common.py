import json
from http import HTTPStatus
from typing import Callable, Dict, List, Optional, Type, Union

from fastapi import HTTPException
from helpers.elastic_helper import page_dict_to_es, sort_query_to_es
from helpers.query_params_helper import (FilterSortWithPaginationParamModel,
                                         ParamsModel,
                                         QueryWithPaginationParamModel)
from models.utils import BaseOrjsonModel
from pydantic import BaseModel
from services.interfaces import (AsyncCacheStorage, AsyncFulltextDB,
                                 GetListAndEntityService)


class FetchListAndEntityWithCacheService(GetListAndEntityService):
    cache_expires_in_seconds = 60 * 5
    index_name: str
    search_fields: List[str]
    sort_fields: List[str]
    object_class: Type[BaseOrjsonModel]
    function_for_request_body_mapping: Optional[
        Callable[
            [
                Union[
                    FilterSortWithPaginationParamModel,
                    ParamsModel,
                    QueryWithPaginationParamModel,
                ],
                Optional[List[str]],
            ],
            Dict,
        ]
    ]

    def __init__(self, cache_storage: AsyncCacheStorage, fulltext_db: AsyncFulltextDB):
        self.cache_storage = cache_storage
        self.fulltext_db = fulltext_db

    async def get_items_list(
        self,
        params: Union[
            FilterSortWithPaginationParamModel,
            ParamsModel,
            QueryWithPaginationParamModel,
        ],
    ) -> Optional[List[BaseOrjsonModel]]:
        items = await self._get_items_list_from_cache(params)
        if not items:
            items = await self._get_items_list_from_full_text_db(params)
            if not items:
                return None
            await self._put_items_list_to_cache(params, items)
        return items

    async def get_by_id(
        self, item_id: str
    ) -> Optional[Union[BaseOrjsonModel, BaseModel]]:
        entity = await self._item_from_cache(item_id)
        if not entity:
            entity = await self._get_item_from_fulltext_db(item_id)
            if not entity:
                return None
            await self._put_item_to_cache(key=item_id, item=entity)
        return entity

    async def _put_items_list_to_cache(
        self,
        params: Union[ParamsModel, str],
        items_list: List[BaseOrjsonModel],
    ):
        await self.cache_storage.set(
            key=self.index_name + str(params),
            value=json.dumps([item.dict() for item in items_list]),
            expire=self.cache_expires_in_seconds,
        )

    async def _put_item_to_cache(self, key: str, item: BaseOrjsonModel):
        await self.cache_storage.set(
            key=key, value=item.json(), expire=self.cache_expires_in_seconds
        )

    async def _get_items_list_from_full_text_db(
        self,
        params: Union[
            FilterSortWithPaginationParamModel,
            ParamsModel,
            QueryWithPaginationParamModel,
        ],
    ) -> List[BaseOrjsonModel]:

        if (
            isinstance(params, ParamsModel)
            and params.sort
            and params.sort.strip("-") not in self.sort_fields
        ):
            fields_for_sort = ", ".join(self.sort_fields)
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"You can sort ONLY by fields: {fields_for_sort}",
            )

        query_body = self.function_for_request_body_mapping(params, self.search_fields)
        docs = await self.fulltext_db.search(
            index=self.index_name,
            body=query_body,
            sort=None
            if isinstance(params, QueryWithPaginationParamModel)
            else sort_query_to_es(params.sort),
            **page_dict_to_es(params.page_number, params.page_size),
        )
        items = [self.object_class(**doc["_source"]) for doc in docs["hits"]["hits"]]
        return items

    async def _get_items_list_from_cache(
        self,
        params: Union[FilterSortWithPaginationParamModel, ParamsModel, str],
        object_class: Type = None,
    ) -> Optional[List[BaseOrjsonModel]]:
        data_list = await self.cache_storage.get(key=self.index_name + str(params))
        if not data_list:
            return None
        object_class = object_class if object_class else self.object_class
        items = [object_class(**data) for data in json.loads(data_list)]
        return items

    async def _item_from_cache(self, item_id: str) -> Optional[BaseOrjsonModel]:
        data = await self.cache_storage.get(key=item_id)
        if not data:
            return None
        film = self.object_class.parse_raw(data)
        return film

    async def _get_item_from_fulltext_db(
        self, item_id: str
    ) -> Optional[BaseOrjsonModel]:
        try:
            doc = await self.fulltext_db.get(self.index_name, item_id)
        except Exception:
            raise HTTPException(
                HTTPStatus.NOT_FOUND,
                "Item doesn't exist, check if uuid is valid",
            )
        return self.object_class(**doc["_source"])
