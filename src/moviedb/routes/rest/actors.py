from fastapi import APIRouter, Depends
from fastapi_pagination import Page, pagination_ctx

from moviedb.core.db.conn import SessionLocal
from moviedb.core.db.models import Actor
from moviedb.schemas.actors import ActorCreate, ActorRead

from .utils import get_row_or_404, paginate_rows

router = APIRouter(prefix="/actors", tags=["actors"])

ListPage = Page[ActorRead]
list_pagination = Depends(pagination_ctx(ListPage))


@router.get("/", dependencies=[list_pagination])
def list_actors() -> ListPage:
    with SessionLocal() as session:
        return paginate_rows(session, Actor, ActorRead)


@router.get("/{actor_id}")
def get_actor(actor_id: int) -> ActorRead:
    with SessionLocal() as session:
        return ActorRead.model_validate(
            get_row_or_404(session, Actor, "actor", actor_id)
        )


@router.post("/", status_code=201)
def create_actor(actor: ActorCreate) -> ActorRead:
    with SessionLocal() as session:
        db_actor = Actor(**actor.model_dump())
        session.add(db_actor)
        session.commit()
        session.refresh(db_actor)
        return ActorRead.model_validate(db_actor)
