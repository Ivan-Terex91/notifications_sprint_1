from typing import List

from models.film import FilmForNotification
from models.user import User
from pydantic import BaseModel


class BookmarksEvent(BaseModel):
    """Модель cобытия с закладками"""

    user: User
    films: List[FilmForNotification]
