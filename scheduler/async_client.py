import asyncio
from http.client import OK
from os import getenv

import httpx
import orjson
from models.film import FilmForNotification
from models.user import User

ugc_url = getenv("UGC_URL")
bookmark_api_prefix = getenv("BOOKMARK_API_PREFIX", "/api/v1/bookmark/")
ugc_timeout = float(getenv("UGC_TIMEOUT", 60.0))

auth_url = getenv("AUTH_URL")
profile_api_prefix = getenv("PROFILE_API_PREFIX", "/api/v1/profile/")

movie_search_url = getenv("MOVIE_SEARCH_URL")
film_api_prefix = getenv("FILM_API_PREFIX", "/api/v1/film/")


async def get_bookmarks_per_user():
    async with httpx.AsyncClient(timeout=ugc_timeout) as client:
        response = await client.get(
            f"{ugc_url}{bookmark_api_prefix}list_bookmarks_per_user/",
            timeout=httpx.Timeout(timeout=ugc_timeout),
        )
        content = orjson.loads(response.content)
    return content


async def get_user(id):
    async with httpx.AsyncClient() as client:
        url = f"{auth_url}{profile_api_prefix}"
        response = await client.post(url, json={"id": id})
    return User.parse_obj(orjson.loads(response.content))


async def get_film(id):
    async with httpx.AsyncClient() as client:
        url = f"{movie_search_url}{film_api_prefix}{id}"
        response = await client.get(url)
        if response.status_code > OK:
            return None
    return orjson.loads(response.content)


async def gather_films(movies):
    tasks = []
    for film_id in movies:
        tasks.append(asyncio.create_task(get_film(film_id)))
    films = await asyncio.gather(*tasks)
    films = [FilmForNotification.parse_obj(film) for film in films if film is not None]
    return films
