from fastapi import APIRouter
from sqlalchemy import select

from moviedb.core.db.conn import SessionLocal
from moviedb.core.db.models import MpaaRating
from .utils import get_row_or_404, serialize_row, serialize_rows

router = APIRouter(prefix="/mpaa-ratings", tags=["mpaa-ratings"])


@router.get("/")
def list_mpaa_ratings() -> list[dict[str, object]]:
    with SessionLocal() as session:
        return serialize_rows(session.scalars(select(MpaaRating)).all())


@router.get("/{entity_id}")
def get_mpaa_rating(entity_id: int) -> dict[str, object]:
    with SessionLocal() as session:
        return serialize_row(
            get_row_or_404(session, MpaaRating, "mpaa_rating", entity_id)
        )
