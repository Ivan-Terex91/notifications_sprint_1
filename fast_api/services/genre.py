from functools import lru_cache

from db.elastic import get_elastic
from db.redis import get_redis
from fastapi import Depends
from helpers.elastic_helper import es_search_request_body
from models.genre import Genre

from .common import FetchListAndEntityWithCacheService
from .interfaces import AsyncCacheStorage, AsyncFulltextDB


class GenreService(FetchListAndEntityWithCacheService):
    index_name = "genres"
    search_fields = ["name"]
    sort_fields = ["name"]
    object_class = Genre
    function_for_request_body_mapping = es_search_request_body


@lru_cache()
def get_genre_service(
    cache_storage: AsyncCacheStorage = Depends(get_redis),
    full_text_db: AsyncFulltextDB = Depends(get_elastic),
) -> GenreService:
    """
    :param cache_storage: Async cache storage
    :param full_text_db: Async full text database
    :return:
    """
    return GenreService(cache_storage, full_text_db)
