from enum import Enum

from api.v1.models.review import AddReviewModel, UserRatingReview
from core.auth import auth_current_user
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import ORJSONResponse
from models.rating import MovieRatingModel
from pydantic import UUID4
from services.rating import RatingService, get_rating_service
from services.review import ReviewService, get_review_service
from starlette import status

router = APIRouter()


class SortFields(Enum):
    rating__asc = "rating"
    rating__desc = "-rating"
    created_at__asc = "created_at"
    created_at__desc = "-created_at"


@router.post(path="/add_review/")
async def add_movie_review(
    review: AddReviewModel,
    rating_service: RatingService = Depends(get_rating_service),
    review_service: ReviewService = Depends(get_review_service),
    auth_user=Depends(auth_current_user),
):
    """Добавление рецензии к фильму"""
    if await review_service.add_review(
        movie_id=review.movie_id,
        user_id=auth_user,
        text=review.text,
        rating=review.rating,
    ):
        movie_rating = MovieRatingModel(
            movie_id=review.movie_id, user_id=auth_user, rating=review.rating
        )
        await rating_service.add_rating(**movie_rating.dict())
        return ORJSONResponse(status_code=status.HTTP_201_CREATED)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"review for movie {review.movie_id} already exists",
    )


@router.patch(path="/{review_id:str}/add_review_rating/")
async def add_or_update_review_rating(
    review_id: str,
    user_rating_review: UserRatingReview,
    review_service: ReviewService = Depends(get_review_service),
    auth_user=Depends(auth_current_user),
):
    """Добавление или обновленик оценки к рецензии"""
    if await review_service.add_or_update_review_rating(
        review_id=review_id, user_id=auth_user, rating=user_rating_review.rating
    ):
        return ORJSONResponse(status_code=status.HTTP_200_OK)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"review {review_id} not found"
    )


@router.get(path="/{movie_id:uuid}/list_review/")
async def list_movie_review(
    movie_id: UUID4,
    sort: SortFields = SortFields.created_at__asc,
    review_service: ReviewService = Depends(get_review_service),
    auth_user=Depends(auth_current_user),
):
    """Список рецензий к фильму"""
    sort_value, sort_order_str = sort.name.split("__")
    sort_order_int = 1 if sort_order_str == "asc" else -1
    return await review_service.get_film_reviews(
        movie_id=movie_id, sort_value=sort_value, sort_order=sort_order_int
    )
