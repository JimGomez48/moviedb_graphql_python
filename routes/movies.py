from fastapi import APIRouter
from sqlalchemy import select

from db.conn import SessionLocal
from db.models import Movie
from routes.common import get_row_or_404, serialize_row, serialize_rows

router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("/")
def list_movies() -> list[dict[str, object]]:
    with SessionLocal() as session:
        return serialize_rows(session.scalars(select(Movie)).all())


@router.get("/{entity_id}")
def get_movie(entity_id: int) -> dict[str, object]:
    with SessionLocal() as session:
        return serialize_row(
            get_row_or_404(session, Movie, "movie", entity_id)
        )