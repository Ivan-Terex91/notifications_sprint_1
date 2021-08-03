from pydantic import BaseModel


class GenreForNotification(BaseModel):
    """Модель жанра для уведомления"""

    name: str
