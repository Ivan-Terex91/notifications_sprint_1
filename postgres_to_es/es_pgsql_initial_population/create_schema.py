from time import sleep

from elasticsearch import Elasticsearch
from move_from_sqlite.logger import logger

elastic = Elasticsearch(hosts=["elasticsearch"])

SETTINGS = {
    "refresh_interval": "1s",
    "analysis": {
        "filter": {
            "english_stop": {"type": "stop", "stopwords": "_english_"},
            "english_stemmer": {"type": "stemmer", "language": "english"},
            "english_possessive_stemmer": {
                "type": "stemmer",
                "language": "possessive_english",
            },
            "russian_stop": {"type": "stop", "stopwords": "_russian_"},
            "russian_stemmer": {"type": "stemmer", "language": "russian"},
        },
        "analyzer": {
            "ru_en": {
                "tokenizer": "standard",
                "filter": [
                    "lowercase",
                    "english_stop",
                    "english_stemmer",
                    "english_possessive_stemmer",
                    "russian_stop",
                    "russian_stemmer",
                ],
            }
        },
    },
}

MAPPING_MOVIES = {
    "settings": SETTINGS,
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "uuid": {"type": "keyword"},
            "imdb_rating": {"type": "float"},
            "genres_titles": {"type": "keyword"},
            "genres": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                    "uuid": {"type": "keyword"},
                    "name": {"type": "text", "analyzer": "ru_en"},
                },
            },
            "title": {
                "type": "text",
                "analyzer": "ru_en",
                "fields": {"raw": {"type": "keyword"}},
            },
            "description": {"type": "text", "analyzer": "ru_en"},
            "directors_names": {"type": "text", "analyzer": "ru_en"},
            "actors_names": {"type": "text", "analyzer": "ru_en"},
            "writers_names": {"type": "text", "analyzer": "ru_en"},
            "directors": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                    "uuid": {"type": "keyword"},
                    "full_name": {"type": "text", "analyzer": "ru_en"},
                },
            },
            "actors": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                    "uuid": {"type": "keyword"},
                    "full_name": {"type": "text", "analyzer": "ru_en"},
                },
            },
            "writers": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                    "uuid": {"type": "keyword"},
                    "full_name": {"type": "text", "analyzer": "ru_en"},
                },
            },
        },
    },
}

MAPPING_GENRES = {
    "settings": SETTINGS,
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "uuid": {"type": "keyword"},
            "name": {"type": "text", "analyzer": "ru_en", "fielddata": "true"},
        },
    },
}

MAPPING_PERSON = {
    "settings": SETTINGS,
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "uuid": {"type": "keyword"},
            "full_name": {"type": "text", "analyzer": "ru_en", "fielddata": "true"},
            "films_directed": {"type": "keyword"},
            "films_acted": {"type": "keyword"},
            "films_written": {"type": "keyword"},
        },
    },
}


def build_index(name: str, mapping: dict) -> None:
    _ = elastic.indices.delete(index=name, ignore=[400, 404])
    response = elastic.indices.create(index=name, body=mapping, ignore=400)

    if "acknowledged" in response:
        if response["acknowledged"]:
            logger.info("Индекст создан: {}".format(response["index"]))
    elif "error" in response:
        logger.error("Ошибка: {}".format(response["error"]["root_cause"]))
    logger.info(response)


if __name__ == "__main__":
    while not elastic.ping():
        logger.error("Still not ready ES...")
        sleep(2)

    indexes = (
        ("movies", MAPPING_MOVIES),
        ("genres", MAPPING_GENRES),
        ("persons", MAPPING_PERSON),
    )
    for index_name, index_mapping in indexes:
        build_index(name=index_name, mapping=index_mapping)
