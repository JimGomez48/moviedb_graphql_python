from fastapi import APIRouter, Depends
from fastapi_pagination import Page, pagination_ctx

from moviedb.dependencies import MovieServiceDep
from moviedb.schemas.movies import MovieCreate, MovieRead

router = APIRouter(prefix="/movies", tags=["movies"])

ListPage = Page[MovieRead]
list_pagination = Depends(pagination_ctx(ListPage))


@router.get("/", dependencies=[list_pagination])
def list_movies(service: MovieServiceDep) -> ListPage:
    return service.list()


@router.get("/{movie_id}")
def get_movie(movie_id: int, service: MovieServiceDep) -> MovieRead:
    return service.get(movie_id)


@router.post("/", status_code=201)
def create_movie(movie: MovieCreate, service: MovieServiceDep) -> MovieRead:
    return service.create(movie)
