from typing import List

from utilities import BaseOrjsonModel


class Person(BaseOrjsonModel):
    uuid: str
    full_name: str
    films_directed: List[str]
    films_acted: List[str]
    films_written: List[str]
