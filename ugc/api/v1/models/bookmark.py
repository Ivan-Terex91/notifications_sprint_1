from pydantic import UUID4, BaseModel


class MovieBookmark(BaseModel):
    """Модель закладок фильма"""

    movie_id: UUID4

    class Config:
        schema_extra = {
            "example": {
                "movie_id": "2831e77b-463d-4678-b261-cb52684db28a",
            }
        }
