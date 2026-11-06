from fastapi import APIRouter
from fastapi_pagination import Page

from moviedb.dependencies import ActorServiceDep
from moviedb.routes.rest.pagination import PageParamsDep, to_page
from moviedb.schemas.actors import ActorCreate, ActorRead

router = APIRouter(prefix="/actors", tags=["actors"])

ListPage = Page[ActorRead]


@router.get("/")
def list_actors(service: ActorServiceDep, params: PageParamsDep) -> ListPage:
    return to_page(ListPage, service.list(params))


@router.get("/{actor_id}")
def get_actor(actor_id: int, service: ActorServiceDep) -> ActorRead:
    return service.get(actor_id)


@router.post("/", status_code=201)
def create_actor(actor: ActorCreate, service: ActorServiceDep) -> ActorRead:
    return service.create(actor)
