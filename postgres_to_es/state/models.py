from datetime import datetime
from typing import Any

from pydantic import BaseModel

from .base_storage import BaseStorage


class State:
    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        try:
            state = self.storage.retrieve_state()
        except FileNotFoundError:
            state = dict()
        state[key] = value
        self.storage.save_state(state)

    def get_state(self, key: str) -> Any:
        return self.storage.retrieve_state().get(key)


class UpdateStateModel(BaseModel):
    movies_updated: datetime = datetime(1970, 1, 1)
    people_updated: datetime = datetime(1970, 1, 1)
    gender_updated: datetime = datetime(1970, 1, 1)
    are_all_completed: bool = False
