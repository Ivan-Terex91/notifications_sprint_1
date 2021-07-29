from api.v1.models.rating import MovieRatingModel, RatingModel
from core.auth import auth_current_user
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import ORJSONResponse
from pydantic import UUID4
from services.rating import RatingService, get_rating_service
from starlette import status

router = APIRouter()


@router.get(path="/{movie_id:uuid}/count_ratings/")
async def count_movie_rating(
    movie_id: UUID4, rating_service: RatingService = Depends(get_rating_service)
):
    """Количества оценок фильма"""
    count_rating = await rating_service.get_count_rating(movie_id=movie_id)
    return ORJSONResponse(
        content={"count_rating": count_rating}, status_code=status.HTTP_200_OK
    )


@router.get(path="/{movie_id:uuid}/avg_rating/")
async def avg_movie_rating(
    movie_id: UUID4, rating_service: RatingService = Depends(get_rating_service)
):
    """Средняя оценка фильма"""
    avg_rating = await rating_service.get_avg_rating(movie_id=movie_id)
    if avg_rating:
        return ORJSONResponse(
            content={"avg_rating": avg_rating}, status_code=status.HTTP_200_OK
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"rating for movie {movie_id} not found",
    )


@router.post(path="/add_rating/")
async def add_movie_rating(
    movie_rating: MovieRatingModel,
    rating_service: RatingService = Depends(get_rating_service),
    auth_user=Depends(auth_current_user),
):
    """Добавить оценку фильма"""
    if await rating_service.add_rating(
        movie_id=movie_rating.movie_id, user_id=auth_user, rating=movie_rating.rating
    ):
        return ORJSONResponse(status_code=status.HTTP_201_CREATED)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"rating for movie {movie_rating.movie_id} already exists",
    )


@router.patch(path="/{movie_id:uuid}/change_rating/")
async def change_movie_rating(
    movie_id: UUID4,
    rating: RatingModel,
    rating_service: RatingService = Depends(get_rating_service),
    auth_user=Depends(auth_current_user),
):
    """Изменить оценку фильма"""
    if await rating_service.change_rating(
        user_id=auth_user, movie_id=movie_id, rating=rating.rating
    ):
        return ORJSONResponse(status_code=status.HTTP_200_OK)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"rating for movie {movie_id} not found",
    )


@router.delete(path="/{movie_id:uuid}/delete_rating/")
async def delete_movie_rating(
    movie_id: UUID4,
    rating_service: RatingService = Depends(get_rating_service),
    auth_user=Depends(auth_current_user),
):
    """Удалить оценку фильма"""
    if await rating_service.delete_rating(user_id=auth_user, movie_id=movie_id):
        return ORJSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"rating for movie {movie_id} not found",
    )
