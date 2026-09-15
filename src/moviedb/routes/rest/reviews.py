from fastapi import APIRouter, Depends
from fastapi_pagination import Page, pagination_ctx

from moviedb.core.db.conn import SessionLocal
from moviedb.core.db.models import Review
from moviedb.schemas.reviews import ReviewRead

from .utils import get_row_or_404, paginate_rows

router = APIRouter(prefix="/reviews", tags=["reviews"])

ListPage = Page[ReviewRead]
list_pagination = Depends(pagination_ctx(ListPage))


@router.get("/", dependencies=[list_pagination])
def list_reviews() -> ListPage:
    with SessionLocal() as session:
        return paginate_rows(session, Review, ReviewRead)


@router.get("/{entity_id}")
def get_review(entity_id: int) -> ReviewRead:
    with SessionLocal() as session:
        return ReviewRead.model_validate(
            get_row_or_404(session, Review, "review", entity_id)
        )
