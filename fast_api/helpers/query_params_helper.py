from typing import Optional

from fastapi import Depends, Query
from pydantic import BaseModel

DEFAULT_PAGE_PARAMS = {"size": 20, "number": 1}

default_sort_field: Optional[str] = None
default_filter_field: Optional[str] = None


class PaginateModel(BaseModel):
    page_number: Optional[int]
    page_size: Optional[int]


class ParamsModel(PaginateModel):
    query: Optional[str]
    sort: Optional[str]


class FilterSortWithPaginationParamModel(PaginateModel):
    sort: Optional[str]
    genre_filter: Optional[str]


class QueryWithPaginationParamModel(PaginateModel):
    query: Optional[str]


async def parse_pagination(
    page_size: Optional[int] = Query(
        DEFAULT_PAGE_PARAMS["size"],
        alias="page[size]",
        description="Items amount on page",
    ),
    page_number: Optional[int] = Query(
        DEFAULT_PAGE_PARAMS["number"],
        alias="page[number]",
        description="Page number for pagination",
    ),
):
    return PaginateModel(
        page_number=max(int(page_number), 1), page_size=max(int(page_size), 1)
    )


async def parse_filter_sort_with_pagination(
    sort: Optional[str] = Query("-imdb_rating", description="Field for sorting"),
    genre_filter: Optional[str] = Query(
        default_filter_field,
        alias="filter[genre]",
        description="Genre uuid for filtering by genre",
    ),
    pagination=Depends(parse_pagination),
):
    return FilterSortWithPaginationParamModel(
        sort=sort,
        genre_filter=genre_filter,
        page_number=pagination.page_number,
        page_size=pagination.page_size,
    )


async def parse_query_with_pagination(
    query: Optional[str] = Query("action", description="Query string to search"),
    pagination=Depends(parse_pagination),
):
    return QueryWithPaginationParamModel(
        query=query,
        page_number=pagination.page_number,
        page_size=pagination.page_size,
    )


async def parse_list_basic(
    sort: Optional[str] = default_sort_field,
    query: Optional[str] = Query(None, description="Query string to search"),
    pagination=Depends(parse_pagination),
):
    return ParamsModel(
        query=query,
        sort=sort,
        page_number=pagination.page_number,
        page_size=pagination.page_size,
    )
