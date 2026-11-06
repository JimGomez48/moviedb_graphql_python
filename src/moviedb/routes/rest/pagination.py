"""Adapts HTTP query parameters and core paging types to fastapi-pagination."""

from typing import Annotated

from fastapi import Depends, Query
from fastapi_pagination import Page, Params

from moviedb.core.pagination import (
    DEFAULT_PAGE_SIZE,
    MAX_PAGE_SIZE,
    PageParams,
    PageResult,
)


def get_page_params(
    page: Annotated[int, Query(ge=1, description="Page number")] = 1,
    size: Annotated[
        int, Query(ge=1, le=MAX_PAGE_SIZE, description="Page size")
    ] = DEFAULT_PAGE_SIZE,
) -> PageParams:
    return PageParams(page=page, size=size)


PageParamsDep = Annotated[PageParams, Depends(get_page_params)]


def to_page[T](page_type: type[Page[T]], result: PageResult[T]) -> Page[T]:
    params = Params(page=result.params.page, size=result.params.size)
    return page_type.create(result.items, params, total=result.total)
