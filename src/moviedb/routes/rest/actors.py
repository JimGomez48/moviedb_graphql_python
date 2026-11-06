from fastapi import APIRouter, Depends
from fastapi_pagination import Page, pagination_ctx

from moviedb.dependencies import ActorServiceDep
from moviedb.schemas.actors import ActorCreate, ActorRead

router = APIRouter(prefix="/actors", tags=["actors"])

ListPage = Page[ActorRead]
list_pagination = Depends(pagination_ctx(ListPage))


@router.get("/", dependencies=[list_pagination])
def list_actors(service: ActorServiceDep) -> ListPage:
    return service.list()


@router.get("/{actor_id}")
def get_actor(actor_id: int, service: ActorServiceDep) -> ActorRead:
    return service.get(actor_id)


@router.post("/", status_code=201)
def create_actor(actor: ActorCreate, service: ActorServiceDep) -> ActorRead:
    return service.create(actor)
