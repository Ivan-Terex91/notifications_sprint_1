from typing import List

from models.genre import GenreForNotification
from pydantic import BaseModel


class FilmForNotification(BaseModel):
    """Модель фильма для уведомления"""

    title: str
    imdb_rating: float
    genres: List[GenreForNotification]
