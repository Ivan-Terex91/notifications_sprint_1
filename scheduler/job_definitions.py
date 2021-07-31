import asyncio

from async_client import get_bookmarks_per_user, get_user


def new_films_of_week(var_one, var_two):
    print("new_films_of_week")


def saved_films():
    saved_films = asyncio.run(get_bookmarks_per_user())
    for item in saved_films:
        user = asyncio.run(get_user(item["_id"]))
        name = user["first_name"]
        email = user["email"]
        print(name, email)
        if not name:
            name = "Киноман"
