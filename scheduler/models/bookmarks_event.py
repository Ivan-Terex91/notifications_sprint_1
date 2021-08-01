from film import FilmForNotification
from user import User
from utils import BaseOrjsonModel


class BookmarksEvent(BaseOrjsonModel):
    user: User
    films: list[FilmForNotification]
