from fastapi import APIRouter
from fastapi_pagination import Page

from moviedb.dependencies import GenreServiceDep
from moviedb.routes.rest.pagination import PageParamsDep, to_page
from moviedb.schemas.genres import GenreRead

router = APIRouter(prefix="/genres", tags=["genres"])

ListPage = Page[GenreRead]


@router.get("/")
def list_genres(service: GenreServiceDep, params: PageParamsDep) -> ListPage:
    return to_page(ListPage, service.list(params))


@router.get("/{genre_id}")
def get_genre(genre_id: int, service: GenreServiceDep) -> GenreRead:
    return service.get(genre_id)
