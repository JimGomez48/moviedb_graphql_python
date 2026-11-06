from fastapi import APIRouter, Depends
from fastapi_pagination import Page, pagination_ctx

from moviedb.dependencies import DirectorServiceDep
from moviedb.schemas.directors import DirectorRead

router = APIRouter(prefix="/directors", tags=["directors"])

ListPage = Page[DirectorRead]
list_pagination = Depends(pagination_ctx(ListPage))


@router.get("/", dependencies=[list_pagination])
def list_directors(service: DirectorServiceDep) -> ListPage:
    return service.list()


@router.get("/{director_id}")
def get_director(director_id: int, service: DirectorServiceDep) -> DirectorRead:
    return service.get(director_id)
