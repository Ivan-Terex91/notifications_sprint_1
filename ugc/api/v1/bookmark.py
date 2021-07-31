from api.v1.models.bookmark import MovieBookmark
from core.auth import auth_current_user
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import ORJSONResponse
from services.bookmark import BookmarkService, get_bookmark_service
from starlette import status

router = APIRouter()


@router.post(path="/add_movie_bookmark/")
async def add_movie_bookmark(
        movie_bookmark: MovieBookmark,
        bookmark_service: BookmarkService = Depends(get_bookmark_service),
        auth_user=Depends(auth_current_user),
):
    """Добавить фильм в закладки"""
    if await bookmark_service.add_bookmark(
            movie_id=movie_bookmark.movie_id, user_id=auth_user
    ):
        return ORJSONResponse(status_code=status.HTTP_201_CREATED)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"bookmark for movie {movie_bookmark.movie_id} already exists",
    )


@router.delete(path="/delete_movie_bookmark/")
async def delete_movie_bookmark(
        movie_bookmark: MovieBookmark,
        bookmark_service: BookmarkService = Depends(get_bookmark_service),
        auth_user=Depends(auth_current_user),
):
    """Удалить фильм из закладкок"""
    if await bookmark_service.delete_bookmark(
            movie_id=movie_bookmark.movie_id, user_id=auth_user
    ):
        return ORJSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"bookmark for movie {movie_bookmark.movie_id} not found",
    )


@router.get(path="/list_movie_bookmark/")
async def list_movie_bookmark(
        bookmark_service: BookmarkService = Depends(get_bookmark_service),
        auth_user=Depends(auth_current_user),
):
    """Список закладок фильмов"""
    return await bookmark_service.get_list_bookmark(user_id=auth_user)


@router.get(path="/list_bookmarks_per_user/")
async def list_movie_bookmark(
        bookmark_service: BookmarkService = Depends(get_bookmark_service)
):
    """Список фильмов по каждому пользователю"""
    return await bookmark_service.get_list_bookmarks_per_user()
