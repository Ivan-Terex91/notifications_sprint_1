from pydantic import UUID4, BaseModel, Field


class MovieRatingModel(BaseModel):
    """Модель рейтинга фильма"""

    movie_id: UUID4
    rating: float = Field(ge=0, le=10)

    class Config:
        schema_extra = {
            "example": {
                "movie_id": "2831e77b-463d-4678-b261-cb52684db28a",
                "rating": 9.5,
            }
        }


class RatingModel(BaseModel):
    rating: float = Field(ge=0, le=10)
