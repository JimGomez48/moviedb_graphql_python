from fastapi import APIRouter
from sqlalchemy import select

from moviedb.db.conn import SessionLocal
from moviedb.db.models import Company
from .utils import get_row_or_404, serialize_row, serialize_rows

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("/")
def list_companies() -> list[dict[str, object]]:
    with SessionLocal() as session:
        return serialize_rows(session.scalars(select(Company)).all())


@router.get("/{entity_id}")
def get_company(entity_id: int) -> dict[str, object]:
    with SessionLocal() as session:
        return serialize_row(get_row_or_404(session, Company, "company", entity_id))
