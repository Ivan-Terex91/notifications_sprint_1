from .utils import BaseOrjsonModel


class Genre(BaseOrjsonModel):
    uuid: str
    name: str
