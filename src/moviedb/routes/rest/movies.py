from fastapi import APIRouter
from fastapi_pagination import Page

from moviedb.dependencies import MovieServiceDep
from moviedb.routes.rest.pagination import PageParamsDep, to_page
from moviedb.routes.rest.schemas.movies import MovieCreate, MovieRead

router = APIRouter(prefix="/movies", tags=["movies"])

ListPage = Page[MovieRead]


@router.get("/")
def list_movies(service: MovieServiceDep, params: PageParamsDep) -> ListPage:
    return to_page(ListPage, service.list(params), MovieRead.from_domain)


@router.get("/{movie_id}")
def get_movie(movie_id: int, service: MovieServiceDep) -> MovieRead:
    return MovieRead.from_domain(service.get(movie_id))


@router.post("/", status_code=201)
def create_movie(movie: MovieCreate, service: MovieServiceDep) -> MovieRead:
    return MovieRead.from_domain(service.create(movie.to_domain()))
