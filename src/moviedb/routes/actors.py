from fastapi import APIRouter
from sqlalchemy import select

from moviedb.db.conn import SessionLocal
from moviedb.db.models import Actor
from moviedb.routes.common import get_row_or_404, serialize_row, serialize_rows

router = APIRouter(prefix="/actors", tags=["actors"])


@router.get("/")
def list_actors() -> list[dict[str, object]]:
    with SessionLocal() as session:
        return serialize_rows(session.scalars(select(Actor)).all())


@router.get("/{entity_id}")
def get_actor(entity_id: int) -> dict[str, object]:
    with SessionLocal() as session:
        return serialize_row(get_row_or_404(session, Actor, "actor", entity_id))
