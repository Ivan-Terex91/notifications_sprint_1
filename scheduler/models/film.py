from typing import List

from models.actor import Actor
from models.director import Director
from models.genre import Genre, GenreForNotification
from models.utilities import BaseOrjsonModel
from models.writer import Writer


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
    genres: List[GenreForNotification]
