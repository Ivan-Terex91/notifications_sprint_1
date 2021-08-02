from typing import Dict, List, Optional, Union

from helpers.query_params_helper import (FilterSortWithPaginationParamModel,
                                         ParamsModel,
                                         QueryWithPaginationParamModel)


def sort_query_to_es(query: str) -> str:
    return f"{query[1:]}:desc" if query and query.startswith("-") else query


def page_dict_to_es(page_number: int, page_size: int) -> Dict[str, int]:
    from_ = (page_number - 1) * page_size
    return {"size": page_size, "from_": from_}


def es_search_request_body(
    _,
    params: Union[
        FilterSortWithPaginationParamModel,
        ParamsModel,
        QueryWithPaginationParamModel,
    ],
    search_fields: Optional[List[str]] = None,
) -> Dict:
    if isinstance(params, ParamsModel) and params.query:
        return {
            "query": {
                "query_string": {
                    "query": f"{params.query.lower()}",
                    "fields": search_fields,
                }
            }
        }

    elif isinstance(params, FilterSortWithPaginationParamModel) and params.genre_filter:
        return {
            "query": {
                "nested": {
                    "path": "genres",
                    "query": {"match": {"genres.uuid": params.genre_filter}},
                }
            }
        }

    elif isinstance(params, QueryWithPaginationParamModel) and params.query:
        return {
            "query": {
                "multi_match": {
                    "query": params.query,
                    "fuzziness": "auto",
                    "fields": search_fields,
                }
            }
        }

    return {"query": {"match_all": {}}}
