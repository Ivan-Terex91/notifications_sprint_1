from os import getenv

import httpx
import orjson

ugc_url = getenv("UGC_URL")
bookmark_api_prefix = "/api/v1/bookmark/"
ugc_timeout = float(getenv("UGC_TIMEOUT"))

auth_url = getenv("AUTH_URL")
profile_api_prefix = "/api/v1/profile/"


def get_bookmarks_per_user():
    response = httpx.get(
        f"{ugc_url}{bookmark_api_prefix}list_bookmarks_per_user/",
        timeout=httpx.Timeout(timeout=ugc_timeout),
    )
    return orjson.loads(response.content)


def get_user(id):
    url = f"{auth_url}{profile_api_prefix}"
    response = httpx.post(url, json={"id": id})
    return orjson.loads(response.content)
