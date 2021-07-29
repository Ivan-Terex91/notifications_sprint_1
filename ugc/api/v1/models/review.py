from datetime import datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel, Field


class UserRatingReview(BaseModel):
    """Оценка ревью от пользователя"""

    rating: float = Field(ge=0, le=10)

    class Config:
        schema_extra = {"example": {"rating": 7.3}}


class AddReviewModel(BaseModel):
    """Модель добавления рецензии к фильму"""

    movie_id: UUID4
    text: str = Field(min_length=20)
    rating: float = Field(ge=0, le=10)

    class Config:
        schema_extra = {
            "example": {
                "movie_id": "2831e77b-463d-4678-b261-cb52684db28a",
                "text": "Forget that the premise is silly and the acting second-rate because director ...",
                "rating": 9.9,
            }
        }


class ReviewModel(BaseModel):
    """Модель рецензии к фильму"""

    text: str = Field(min_length=20)
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    user_id: UUID4
    movie_id: UUID4
    user_rating_review: List[Optional[UserRatingReview]] = Field(default_factory=list)
    rating: float = Field(ge=0, le=10)
