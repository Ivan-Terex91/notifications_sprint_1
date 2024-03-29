from models.utilities import BaseOrjsonModel


class Genre(BaseOrjsonModel):
    uuid: str
    name: str


class GenreForNotification(BaseOrjsonModel):
    name: str
