from pydantic import UUID4, BaseModel, EmailStr, Field


class RatingReviewEventModel(BaseModel):
    """Модель данных события о оценке ревью"""

    user_review_id: UUID4
    user_rating_id: UUID4
    review_id: UUID4
    rating: float = Field(ge=0, le=10)
    email: EmailStr

    class Config:
        schema_extra = {
            "example": {
                "user_review_id": "2831e77b-463d-4678-b261-cb52684db28a",
                "user_rating_id": "2831e77b-463d-4678-b261-cb52684db28b",
                "review_id": "2831e77b-463d-4678-b261-cb52684db28b",
                "rating": 7.5,
                "email": "Bob@yandex.ru",
            }
        }
