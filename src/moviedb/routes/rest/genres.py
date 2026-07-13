from fastapi import APIRouter
from sqlalchemy import select

from moviedb.core.db.conn import SessionLocal
from moviedb.core.db.models import Genre
from .utils import get_row_or_404, serialize_row, serialize_rows

router = APIRouter(prefix="/genres", tags=["genres"])


@router.get("/")
def list_genres() -> list[dict[str, object]]:
    with SessionLocal() as session:
        return serialize_rows(session.scalars(select(Genre)).all())


@router.get("/{entity_id}")
def get_genre(entity_id: int) -> dict[str, object]:
    with SessionLocal() as session:
        return serialize_row(get_row_or_404(session, Genre, "genre", entity_id))
