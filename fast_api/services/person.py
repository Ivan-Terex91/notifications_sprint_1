from functools import lru_cache
from typing import List, Optional

from db.elastic import get_elastic
from db.redis import get_redis
from fastapi import Depends
from helpers.elastic_helper import es_search_request_body
from models.film import Film
from models.person import Person

from .common import FetchListAndEntityWithCacheService
from .interfaces import AsyncCacheStorage, AsyncFulltextDB

CACHE_PREFIX_FILM_BY_PERSON = "films by person"


class PersonService(FetchListAndEntityWithCacheService):
    index_name = "persons"
    search_fields = ["full_name"]
    sort_fields = ["full_name"]
    object_class = Person
    function_for_request_body_mapping = es_search_request_body

    async def get_films_by_person(self, person_id: str) -> Optional[List[Film]]:
        items = await self._get_items_list_from_cache(
            CACHE_PREFIX_FILM_BY_PERSON + person_id, object_class=Film
        )
        if not items:
            items = await self._get_films_by_person_from_full_text_db(person_id)
            if not items:
                return None
            await self._put_items_list_to_cache(
                CACHE_PREFIX_FILM_BY_PERSON + person_id, items
            )
        return items

    async def _get_films_by_person_from_full_text_db(
        self, person_id: str
    ) -> List[Film]:
        query_body = {
            "query": {
                "bool": {
                    "should": [
                        {
                            "nested": {
                                "path": "directors",
                                "query": {"match": {"directors.uuid": person_id}},
                            }
                        },
                        {
                            "nested": {
                                "path": "writers",
                                "query": {"match": {"writers.uuid": person_id}},
                            }
                        },
                        {
                            "nested": {
                                "path": "actors",
                                "query": {"match": {"actors.uuid": person_id}},
                            }
                        },
                    ]
                }
            }
        }
        docs = await self.fulltext_db.search(index="movies", body=query_body)
        items = [Film(**doc["_source"]) for doc in docs["hits"]["hits"]]
        return items


@lru_cache()
def get_person_service(
    cache_storage: AsyncCacheStorage = Depends(get_redis),
    full_text_db: AsyncFulltextDB = Depends(get_elastic),
) -> PersonService:
    """
    :param cache_storage: Async cache storage
    :param full_text_db: Async full text database
    :return:
    """
    return PersonService(cache_storage, full_text_db)
