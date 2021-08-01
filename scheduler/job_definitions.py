import asyncio

import aio_pika

import config
from async_client import get_bookmarks_per_user, get_user, gather_films
from helpers import publish_bookmarks_event
from models.bookmarks_event import BookmarksEvent

loop = asyncio.new_event_loop()
rabbit_connection = loop.run_until_complete(
    aio_pika.connect_robust(url=config.rabbit_dsnm)
)


def new_films_of_week(var_one, var_two):
    print("new_films_of_week")


def saved_films():
    saved_films = loop.run_until_complete(get_bookmarks_per_user())
    for item in saved_films:
        user = loop.run_until_complete(get_user(item["_id"]))
    films = loop.run_until_complete(gather_films(item["movies"]))

    bookmarks_event = BookmarksEvent(user=user, films=films).json()
    print(bookmarks_event)
    loop.run_until_complete(publish_bookmarks_event(rabbit_connection, bookmarks_event))
