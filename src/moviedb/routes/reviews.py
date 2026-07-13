from fastapi import APIRouter
from sqlalchemy import select

from moviedb.db.conn import SessionLocal
from moviedb.db.models import Review
from moviedb.routes.common import get_row_or_404, serialize_row, serialize_rows

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.get("/")
def list_reviews() -> list[dict[str, object]]:
    with SessionLocal() as session:
        return serialize_rows(session.scalars(select(Review)).all())


@router.get("/{entity_id}")
def get_review(entity_id: int) -> dict[str, object]:
    with SessionLocal() as session:
        return serialize_row(get_row_or_404(session, Review, "review", entity_id))
