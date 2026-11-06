from fastapi import APIRouter, Depends
from fastapi_pagination import Page, pagination_ctx

from moviedb.dependencies import GenreServiceDep
from moviedb.schemas.genres import GenreRead

router = APIRouter(prefix="/genres", tags=["genres"])

ListPage = Page[GenreRead]
list_pagination = Depends(pagination_ctx(ListPage))


@router.get("/", dependencies=[list_pagination])
def list_genres(service: GenreServiceDep) -> ListPage:
    return service.list()


@router.get("/{genre_id}")
def get_genre(genre_id: int, service: GenreServiceDep) -> GenreRead:
    return service.get(genre_id)
