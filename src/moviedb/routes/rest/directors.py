from fastapi import APIRouter
from sqlalchemy import select

from moviedb.db.conn import SessionLocal
from moviedb.db.models import Director
from .utils import get_row_or_404, serialize_row, serialize_rows

router = APIRouter(prefix="/directors", tags=["directors"])


@router.get("/")
def list_directors() -> list[dict[str, object]]:
    with SessionLocal() as session:
        return serialize_rows(session.scalars(select(Director)).all())


@router.get("/{entity_id}")
def get_director(entity_id: int) -> dict[str, object]:
    with SessionLocal() as session:
        return serialize_row(get_row_or_404(session, Director, "director", entity_id))
