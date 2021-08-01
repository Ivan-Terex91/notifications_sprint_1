from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from helpers import query_params_helper as qh
from models.film import ShortFilm
from models.person import Person
from services.common import GetListAndEntityService
from services.person import PersonService, get_person_service

router = APIRouter()
qh.default_sort_field = "name"

PEOPLE_NOT_FOUND = "people or person not found"
FILMS_FOR_PERSON_NOT_FOUND = "films for person not found"


@router.get(
    "/search/",
    response_model=List[Person],
    summary="List of people",
    description="List of people with sorting and searching",
    response_description="People list",
)
async def people_list(
    params: qh.ParamsModel = Depends(qh.parse_list_basic),
    service: GetListAndEntityService = Depends(get_person_service),
) -> List[Person]:
    people = await service.get_items_list(params=params)
    if not people:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=PEOPLE_NOT_FOUND)
    return [
        Person(
            uuid=person.uuid,
            full_name=person.full_name,
            films_directed=person.films_directed,
            films_acted=person.films_acted,
            films_written=person.films_written,
        )
        for person in people
    ]


@router.get(
    "/{person_id}/film/",
    response_model=List[ShortFilm],
    summary="List of films by person",
    description="List of films according to exact person",
    response_description="Films list by person",
)
async def person_films_list(
    person_id: str, service: PersonService = Depends(get_person_service)
) -> List[ShortFilm]:
    films = await service.get_films_by_person(person_id=person_id)
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=FILMS_FOR_PERSON_NOT_FOUND
        )
    return [
        ShortFilm(uuid=film.uuid, title=film.title, imdb_rating=film.imdb_rating)
        for film in films
    ]


@router.get(
    "/{person_id}/",
    response_model=Person,
    summary="Person details",
    description="Person details with played, directed and written films",
    response_description="Person with films by person id",
)
async def person_details(
    person_id: str,
    service: GetListAndEntityService = Depends(get_person_service),
) -> Person:
    person = await service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=PEOPLE_NOT_FOUND)
    return Person(
        uuid=person.uuid,
        full_name=person.full_name,
        films_directed=person.films_directed,
        films_acted=person.films_acted,
        films_written=person.films_written,
    )
