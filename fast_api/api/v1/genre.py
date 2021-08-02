from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from helpers import query_params_helper as qh
from models.genre import Genre
from services.common import GetListAndEntityService
from services.genre import GenreService, get_genre_service

router = APIRouter()
qh.default_sort_field = "name"

GENRES_NOT_FOUND = "genres not found"


@router.get(
    "/",
    response_model=List[Genre],
    summary="Genres list",
    description="List of all available genres with search and sorting",
    response_description="Genres list",
)
async def genres_list(
    params: qh.ParamsModel = Depends(qh.parse_list_basic),
    service: GetListAndEntityService = Depends(get_genre_service),
) -> List[Genre]:
    genres = await service.get_items_list(params=params)
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=GENRES_NOT_FOUND)
    return [Genre(uuid=genre.uuid, name=genre.name) for genre in genres]


@router.get(
    "/{genre_id}",
    response_model=Genre,
    summary="Genre details",
    description="Genre description by id",
    response_description="Genre description",
)
async def genre_details(
    genre_id: str,
    service: GetListAndEntityService = Depends(get_genre_service),
) -> Genre:
    genre = await service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=GENRES_NOT_FOUND)
    return Genre(uuid=genre.uuid, name=genre.name)
