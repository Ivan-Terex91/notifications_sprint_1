from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from helpers import query_params_helper as qh
from models.film import Film, ShortFilm
from services.film import get_film_service
from services.interfaces import GetListAndEntityService

FILM_NOT_FOUND = "film not found"

router = APIRouter()


@router.get(
    "/{film_id}",
    response_model=Film,
    summary="Film details",
    description="Film details with title, imdb_rating, description, persons, genres",
    response_description="Film with details by id",
)
async def film_details(
    film_id: str,
    film_service: GetListAndEntityService = Depends(get_film_service),
) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FILM_NOT_FOUND)
    return film


@router.get(
    "/",
    response_model=List[ShortFilm],
    summary="List of films",
    description="List of films, can be filtered by genre id",
    response_description="Short information about each film",
)
async def films_list(
    params: qh.FilterSortWithPaginationParamModel = Depends(
        qh.parse_filter_sort_with_pagination
    ),
    film_service: GetListAndEntityService = Depends(get_film_service),
) -> List[ShortFilm]:
    films = await film_service.get_items_list(params=params)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FILM_NOT_FOUND)
    return [
        ShortFilm(uuid=film.uuid, title=film.title, imdb_rating=film.imdb_rating)
        for film in films
    ]


@router.get(
    "/search/",
    response_model=List[ShortFilm],
    summary="List of films for query ranked accordingly",
    description="List of films ranked by title, description, genres_titles, persons",
    response_description="Relevant films list",
)
async def films_list(
    params: qh.QueryWithPaginationParamModel = Depends(qh.parse_query_with_pagination),
    film_service: GetListAndEntityService = Depends(get_film_service),
) -> List[ShortFilm]:
    films = await film_service.get_items_list(params=params)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FILM_NOT_FOUND)
    return [
        ShortFilm(uuid=film.uuid, title=film.title, imdb_rating=film.imdb_rating)
        for film in films
    ]
