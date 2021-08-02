from functools import lru_cache

from db.elastic import get_elastic
from db.redis import get_redis
from fastapi import Depends
from helpers.elastic_helper import es_search_request_body
from models.film import Film
from services.common import FetchListAndEntityWithCacheService
from services.interfaces import AsyncCacheStorage, AsyncFulltextDB

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class FilmService(FetchListAndEntityWithCacheService):
    index_name = "movies"
    search_fields = [
        "title^5",
        "description^4",
        "genres_titles^3",
        "actors_names^3",
        "writers_names^2",
        "directors_names",
    ]
    sort_fields = ["imdb_rating"]
    object_class = Film
    function_for_request_body_mapping = es_search_request_body


@lru_cache()
def get_film_service(
    cache_storage: AsyncCacheStorage = Depends(get_redis),
    full_text_db: AsyncFulltextDB = Depends(get_elastic),
) -> FilmService:
    """
    :param cache_storage: Async cache storage
    :param full_text_db: Async full text database
    :return:
    """
    return FilmService(cache_storage, full_text_db)
