from functools import wraps

import psycopg2
from es_pgsql_initial_population.move_from_sqlite.db_settings import DSL
from psycopg2.extras import DictCursor


def psycopg2_cursor(func):
    @wraps(func)
    def inner(*args, **kwargs):
        with psycopg2.connect(**DSL) as conn:
            cur = conn.cursor(cursor_factory=DictCursor)
            fn = func(cursor=cur, *args, **kwargs)
        return fn

    return inner
