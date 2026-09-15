from fastapi import APIRouter, Depends
from fastapi_pagination import Page, pagination_ctx

from moviedb.core.db.conn import SessionLocal
from moviedb.core.db.models import MpaaRating
from moviedb.schemas.mpaa_ratings import MpaaRatingRead

from .utils import get_row_or_404, paginate_rows

router = APIRouter(prefix="/mpaa-ratings", tags=["mpaa-ratings"])

ListPage = Page[MpaaRatingRead]
list_pagination = Depends(pagination_ctx(ListPage))


@router.get("/", dependencies=[list_pagination])
def list_mpaa_ratings() -> ListPage:
    with SessionLocal() as session:
        return paginate_rows(session, MpaaRating, MpaaRatingRead)


@router.get("/{entity_id}")
def get_mpaa_rating(entity_id: int) -> MpaaRatingRead:
    with SessionLocal() as session:
        return MpaaRatingRead.model_validate(
            get_row_or_404(session, MpaaRating, "mpaa_rating", entity_id)
        )
