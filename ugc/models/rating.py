from pydantic import UUID4, BaseModel, Field


class MovieRatingModel(BaseModel):
    """Модель рейтинга фильма"""

    user_id: UUID4
    movie_id: UUID4
    rating: float = Field(ge=0, le=10)
