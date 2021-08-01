from typing import List

from film import FilmForNotification
from user import User
from utilities import BaseOrjsonModel


class BookmarksEvent(BaseOrjsonModel):
    user: User
    films: List[FilmForNotification]
