from pydantic import UUID4, BaseModel


class MovieBookmark(BaseModel):
    """Модель закладок фильма"""

    user_id: UUID4
    movie_id: UUID4
