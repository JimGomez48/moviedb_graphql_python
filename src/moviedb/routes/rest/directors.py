from fastapi import APIRouter
from fastapi_pagination import Page

from moviedb.dependencies import DirectorServiceDep
from moviedb.routes.rest.pagination import PageParamsDep, to_page
from moviedb.schemas.directors import DirectorRead

router = APIRouter(prefix="/directors", tags=["directors"])

ListPage = Page[DirectorRead]


@router.get("/")
def list_directors(service: DirectorServiceDep, params: PageParamsDep) -> ListPage:
    return to_page(ListPage, service.list(params))


@router.get("/{director_id}")
def get_director(director_id: int, service: DirectorServiceDep) -> DirectorRead:
    return service.get(director_id)
