from typing import List, Optional

from .actor import Actor
from .director import Director
from .genre import Genre, GenreForNotification
from .utils import BaseOrjsonModel
from .writer import Writer


class ShortFilm(BaseOrjsonModel):
    uuid: str
    title: str
    imdb_rating: float


class Film(ShortFilm):
    description: str
    genres: List[Genre]
    actors: List[Actor]
    writers: List[Writer]
    directors: List[Director]


class FilmForNotification(BaseOrjsonModel):
    title: str
    imdb_rating: float
    genres: list[GenreForNotification]
