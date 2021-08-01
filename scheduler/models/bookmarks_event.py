from typing import List

from models.film import FilmForNotification
from models.user import User
from models.utilities import BaseOrjsonModel


class BookmarksEvent(BaseOrjsonModel):
    user: User
    films: List[FilmForNotification]
