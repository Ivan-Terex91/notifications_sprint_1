import json
import os
from datetime import datetime
from time import sleep
from typing import Coroutine

from elasticsearch import Elasticsearch, helpers
from es_pgsql_initial_population.move_from_sqlite.db_settings import (
    GENRE_TABLE, MOVIE_TABLE, MOVIES_ACTORS_M2M_TABLE,
    MOVIES_DIRECTORS_M2M_TABLE, MOVIES_GENRES_M2M_TABLE,
    MOVIES_WRITERS_M2M_TABLE, PERSON_TABLE, SCHEMA)
from es_pgsql_initial_population.move_from_sqlite.logger import logger
from helpers.backoff import backoff
from helpers.connect_psycopg import psycopg2_cursor
from helpers.coroutine_wrapper import coroutine
from psycopg2.extras import DictCursor
from state.json_file_storage import JsonFileStorage
from state.models import State, UpdateStateModel

SLEEP_TIME_SECONDS = 30
MAX_BATCH_AMOUNT = 100

es = Elasticsearch(hosts=[os.getenv("ELASTIC_HOST", "127.0.0.1")])


@coroutine
def write_to_es(state: State) -> Coroutine:
    """
    movies - set of updates movies IDs
    :return:
    """
    while True:
        last_update_state, movies = yield
        logger.info("Send all data to ES")
        actions = []
        for movie in movies:
            logger.info(f"""Process movie: {movie['title']}""")
            actors = (
                [
                    {"uuid": _id, "full_name": name}
                    for _id, name in zip(
                        movie["actors_ids"].split(","),
                        movie["actors_names"].split(","),
                    )
                ]
                if movie["actors_ids"]
                else []
            )
            directors = (
                [
                    {"uuid": _id, "full_name": name}
                    for _id, name in zip(
                        movie["directors_ids"].split(","),
                        movie["directors_names"].split(","),
                    )
                ]
                if movie["directors_ids"]
                else []
            )
            writers = (
                [
                    {"uuid": _id, "full_name": name}
                    for _id, name in zip(
                        movie["writers_ids"].split(","),
                        movie["writers_names"].split(","),
                    )
                ]
                if movie["writers_ids"]
                else []
            )
            genres = (
                [
                    {"uuid": _id, "name": name}
                    for _id, name in zip(
                        movie["genres_ids"].split(","),
                        movie["genres_titles"].split(","),
                    )
                ]
                if movie["genres_ids"]
                else []
            )
            action = {
                "_index": "movies",
                "_id": movie["id"],
                "_source": {
                    "uuid": movie["id"],
                    "imdb_rating": float(movie["imdb_rating"]),
                    "genres_titles": movie["genres_titles"],
                    "title": movie["title"],
                    "description": movie["description"],
                    "directors_names": movie["directors_names"],
                    "actors_names": movie["actors_names"],
                    "writers_names": movie["writers_names"],
                    "genres": genres,
                    "directors": directors,
                    "actors": actors,
                    "writers": writers,
                },
            }
            actions.append(action)

        helpers.bulk(es, actions)
        logger.info(f"Transfer completed, {len(movies)} updated...")
        if last_update_state.are_all_completed:
            logger.info(f"Transfer completed, all records updated")
            last_update_state.are_all_completed = False
            state.set_state("last_update_state", last_update_state.json())


@coroutine
@psycopg2_cursor
def final_fetch_all_changed_movies(
    cursor: DictCursor, next_pipe: Coroutine
) -> Coroutine:
    """
    movies_ids - set of updates movies IDs
    timestamp - time threshold for update
    :return:
    """
    while True:
        last_update_state, movies_ids = yield
        logger.info(
            f"Fetching all updated movies " f"{last_update_state.movies_updated}"
        )
        if movies_ids == set():
            continue
        sql = f"""
                WITH actors_list as (
                    SELECT m.id,
                    string_agg(TRIM(CONCAT(a.last_name || ' ', a.first_name)), ',') as actors,
                    string_agg(a.id::varchar, ',') as actors_ids
                        FROM {SCHEMA}.{MOVIE_TABLE} m
                        LEFT JOIN {SCHEMA}.{MOVIES_ACTORS_M2M_TABLE} ma on m.id = ma.movie_id
                        LEFT JOIN {SCHEMA}.{PERSON_TABLE} a on ma.person_id = a.id
                    GROUP BY m.id
                ),
                directors_list as (
                    SELECT m.id,
                    string_agg(TRIM(CONCAT(a.last_name || ' ', a.first_name)), ',') as directors,
                    string_agg(a.id::varchar, ',') as directors_ids
                        FROM {SCHEMA}.{MOVIE_TABLE} m
                        LEFT JOIN {SCHEMA}.{MOVIES_DIRECTORS_M2M_TABLE} ma on m.id = ma.movie_id
                        LEFT JOIN {SCHEMA}.{PERSON_TABLE} a on ma.person_id = a.id
                    GROUP BY m.id
                ),
                writers_list as (
                    SELECT m.id,
                    string_agg(TRIM(CONCAT(a.last_name || ' ', a.first_name)), ',') as writers,
                    string_agg(a.id::varchar, ',') as writers_ids
                        FROM {SCHEMA}.{MOVIE_TABLE} m
                        LEFT JOIN {SCHEMA}.{MOVIES_WRITERS_M2M_TABLE} mw on m.id = mw.movie_id
                        LEFT JOIN {SCHEMA}.{PERSON_TABLE} a on mw.person_id = a.id
                    GROUP BY m.id
                ),
                genres_list as (
                    SELECT m.id,
                    string_agg(g.title, ',') as genres,
                    string_agg(g.id::varchar, ',') as genres_ids
                        FROM {SCHEMA}.{MOVIE_TABLE} m
                        LEFT JOIN {SCHEMA}.{MOVIES_GENRES_M2M_TABLE} mg on m.id = mg.movie_id
                        LEFT JOIN {SCHEMA}.{GENRE_TABLE} g on mg.genre_id = g.id
                    GROUP BY m.id
                )
                SELECT m.id,
                m.imdb_rating,
                m.title,
                m.imdb_rating,
                m.description,
                actors_list.actors as actors_names,
                actors_list.actors_ids as actors_ids,
                directors_list.directors as directors_names,
                directors_list.directors_ids as directors_ids,
                writers_list.writers as writers_names,
                writers_list.writers_ids as writers_ids,
                genres_list.genres as genres_titles,
                genres_list.genres_ids as genres_ids
                FROM {SCHEMA}.{MOVIE_TABLE} m
                LEFT JOIN actors_list ON m.id = actors_list.id
                LEFT JOIN writers_list ON m.id = writers_list.id
                LEFT JOIN directors_list ON m.id = directors_list.id
                LEFT JOIN genres_list ON m.id = genres_list.id
                WHERE m.id::varchar IN %(movies)s
            """
        cursor.execute(sql, {"movies": tuple(movies_ids)})
        results = cursor.fetchall()
        next_pipe.send((last_update_state, results))


@coroutine
@psycopg2_cursor
def fetch_movies_with_changed_gender(
    cursor: DictCursor, next_pipe: Coroutine
) -> Coroutine:
    """
    Collecting all changes in gender table and
    send assigned movies IDs futher to next coroutine
    movies_ids - set of updates movies IDs
    timestamp - time threshold for update
    At this node of our pipe it's pretty possible to get anourmous
    amount of records, so let's paginate it by MAX_BATCH_AMOUNT.
    Before pagination we're sending all accumulated ids to next pipe
    :return: Coroutine
    """
    while True:
        last_update_state, movies_ids = yield
        logger.info(
            f"Fetching genders changed after " f"{last_update_state.movies_updated}"
        )
        sql_count = f"""
            SELECT count(id) AS amount FROM {SCHEMA}.{MOVIES_GENRES_M2M_TABLE}
            WHERE genre_id IN (
                SELECT p.id as id FROM {SCHEMA}.{GENRE_TABLE} p 
            WHERE p.updated_at > %s
            )
                    """
        cursor.execute(sql_count, (last_update_state.gender_updated,))
        amount_of_ids = cursor.fetchone()["amount"]
        last_update_state.are_all_completed = amount_of_ids == 0
        next_pipe.send((last_update_state, movies_ids))

        offset = 0
        while offset < amount_of_ids:
            sql = f"""
                SELECT movie_id as id FROM {SCHEMA}.{MOVIES_GENRES_M2M_TABLE}
                WHERE genre_id IN (
                          SELECT p.id as id FROM {SCHEMA}.{GENRE_TABLE} p 
                          WHERE p.updated_at > %s
                )
                LIMIT {MAX_BATCH_AMOUNT} OFFSET {offset}
                   """
            cursor.execute(sql, (last_update_state.gender_updated,))
            results = set([x["id"] for x in cursor.fetchall()])

            offset += MAX_BATCH_AMOUNT
            if offset >= amount_of_ids:
                last_update_state.are_all_completed = True
                last_update_state.gender_updated = datetime.now()

            next_pipe.send((last_update_state, results))


@coroutine
@psycopg2_cursor
def fetch_movies_with_changed_people(
    cursor: DictCursor, next_pipe: Coroutine
) -> Coroutine:
    """
    Collecting all changes in actors, directors, writers tables and
    send assigned movies IDs futher to next coroutine
    movies_ids - set of updates movies IDs
    timestamp - time threshold for update
    :return: Coroutine
    """
    tables = (
        f"{SCHEMA}.{MOVIES_ACTORS_M2M_TABLE}",
        f"{SCHEMA}.{MOVIES_DIRECTORS_M2M_TABLE}",
        f"{SCHEMA}.{MOVIES_WRITERS_M2M_TABLE}",
    )
    while True:
        last_update_state, movies_ids = yield
        logger.info(
            f"Fetching people changed after " f"{last_update_state.movies_updated}"
        )
        for table in tables:
            sql = f"""
                     SELECT movie_id as id FROM {table}
                     WHERE person_id IN (
                        SELECT p.id as id FROM {SCHEMA}.{PERSON_TABLE} p 
                        WHERE p.updated_at > %s
                     )
                  """
            cursor.execute(sql, (last_update_state.people_updated,))
            results = set([x["id"] for x in cursor.fetchall()])
            movies_ids = movies_ids.union(results)
        last_update_state.people_updated = datetime.now()
        next_pipe.send((last_update_state, movies_ids))


@coroutine
@psycopg2_cursor
def fetch_changed_movies_ids(cursor: DictCursor, next_pipe: Coroutine) -> Coroutine:
    """
    Collecting all changes in actors, directors, writers tables and
    send assigned movies IDs futher to next coroutine
    timestamp - time threshold for update
    :return: Coroutine
    """
    while last_update_state := (yield):
        logger.info(
            f"Fetching movies changed after " f"{last_update_state.movies_updated}"
        )
        sql = f"""
                 SELECT m.id as id FROM {SCHEMA}.{MOVIE_TABLE} m 
                 WHERE m.updated_at > %s
              """
        cursor.execute(sql, (last_update_state.movies_updated,))
        results = set([x["id"] for x in cursor.fetchall()])
        last_update_state.movies_updated = datetime.now()
        next_pipe.send((last_update_state, results))


@coroutine
@psycopg2_cursor
def fetch_changed_genres(cursor: DictCursor, next_pipe: Coroutine) -> Coroutine:
    """
    Collecting all changes in genres table
    timestamp - time threshold for update
    :return: Coroutine
    """
    while last_genres_updated := (yield):
        logger.info(f"Fetching genres changed after " f"{last_genres_updated}")
        sql = f"""
                 SELECT id, title FROM {SCHEMA}.{GENRE_TABLE} 
                 WHERE updated_at > %s
              """
        cursor.execute(sql, (last_genres_updated,))
        results = cursor.fetchall()
        last_genres_updated = datetime.now()
        next_pipe.send((last_genres_updated, results))


@coroutine
def write_changed_genres_to_es(state: State) -> Coroutine:
    """
    genres - list of updated genres
    :return:
    """
    while True:
        last_genres_updated, genres = yield
        logger.info("Send genres data to ES")
        actions = []
        for genre in genres:
            logger.info(f"""Process genre: {genre['title']}""")
            action = {
                "_index": "genres",
                "_id": genre["id"],
                "_source": {
                    "uuid": genre["id"],
                    "name": genre["title"],
                },
            }
            actions.append(action)

        helpers.bulk(es, actions)
        logger.info(f"Transfer of genres completed, {len(genres)} updated...")
        state.set_state("last_genres_updated", str(last_genres_updated))


@coroutine
@psycopg2_cursor
def fetch_changed_people(cursor: DictCursor, next_pipe: Coroutine) -> Coroutine:
    """
    Collecting all changes in people table
    timestamp - time threshold for update
    :return: Coroutine
    """
    while last_people_updated := (yield):
        logger.info(f"Fetching people changed after " f"{last_people_updated}")
        sql = f"""
                SELECT 
                p.id,
                TRIM(CONCAT(p.last_name || ' ', p.first_name)) as full_name,
                (
                SELECT string_agg(ma.movie_id::varchar, ',')
                    FROM {SCHEMA}.{MOVIES_ACTORS_M2M_TABLE} ma
                    WHERE ma.person_id = p.id
                ) as films_acted,
                (
                SELECT string_agg(md.movie_id::varchar, ',')
                    FROM {SCHEMA}.{MOVIES_DIRECTORS_M2M_TABLE} md
                    WHERE md.person_id = p.id
                ) as films_directed,
                (
                SELECT string_agg(mw.movie_id::varchar, ',')
                    FROM {SCHEMA}.{MOVIES_WRITERS_M2M_TABLE} mw
                    WHERE mw.person_id = p.id
                ) as films_written
                FROM {SCHEMA}.{PERSON_TABLE} p
                WHERE updated_at > %s
              """
        cursor.execute(sql, (last_people_updated,))
        results = cursor.fetchall()
        last_people_updated = datetime.now()
        next_pipe.send((last_people_updated, results))


@coroutine
def write_changed_people_to_es(state: State) -> Coroutine:
    """
    people - list of updated genres
    :return:
    """
    while True:
        last_people_updated, people = yield
        logger.info("Send people data to ES")
        actions = []
        for person in people:
            logger.info(f"""Process person: {person['full_name']}""")
            action = {
                "_index": "persons",
                "_id": person["id"],
                "_source": {
                    "uuid": person["id"],
                    "full_name": person["full_name"],
                    "films_directed": person["films_directed"].split(",")
                    if person["films_directed"]
                    else [],
                    "films_acted": person["films_acted"].split(",")
                    if person["films_acted"]
                    else [],
                    "films_written": person["films_written"].split(",")
                    if person["films_written"]
                    else [],
                },
            }
            actions.append(action)

        helpers.bulk(es, actions)
        logger.info(f"Transfer of people completed, {len(people)} updated...")
        state.set_state("last_people_updated", str(last_people_updated))


@backoff(logger=logger)
def start_process(state: State) -> None:
    """
    Declare coroutines and fire them in eternal loop.
    Update current state in every coroutine and save it in the end of pipe
    :param state: State variable to store update times
    :return:
    """
    write_genres_to_es_coro = write_changed_genres_to_es(state=state)
    fetch_genres = fetch_changed_genres(next_pipe=write_genres_to_es_coro)

    write_people_to_es_coro = write_changed_people_to_es(state=state)
    fetch_people = fetch_changed_people(next_pipe=write_people_to_es_coro)

    write_to_es_coro = write_to_es(state=state)
    final_fetch = final_fetch_all_changed_movies(next_pipe=write_to_es_coro)
    gender_coroutine = fetch_movies_with_changed_gender(next_pipe=final_fetch)
    people_coroutine = fetch_movies_with_changed_people(next_pipe=gender_coroutine)
    movies_coroutine = fetch_changed_movies_ids(next_pipe=people_coroutine)

    while True:
        state_from_storage = state.get_state("last_update_state")
        last_update_state = (
            UpdateStateModel(**json.loads(state_from_storage))
            if state_from_storage
            else UpdateStateModel()
        )
        logger.info("Starting ETL process for updates ...")

        fetch_genres.send(
            state.get_state("last_genres_updated") or str(datetime(1970, 1, 1))
        )
        fetch_people.send(
            state.get_state("last_people_updated") or str(datetime(1970, 1, 1))
        )
        movies_coroutine.send(last_update_state)

        sleep(SLEEP_TIME_SECONDS)


if __name__ == "__main__":
    while not es.ping():
        logger.error("Still not ready ES...")
        sleep(2)
    logger.info("Program started")

    state_common = State(JsonFileStorage(logger=logger))
    start_process(state=state_common)
