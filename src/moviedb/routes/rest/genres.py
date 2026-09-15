from fastapi import APIRouter, Depends
from fastapi_pagination import Page, pagination_ctx

from moviedb.core.db.conn import SessionLocal
from moviedb.core.db.models import Genre
from moviedb.schemas.genres import GenreRead

from .utils import get_row_or_404, paginate_rows

router = APIRouter(prefix="/genres", tags=["genres"])

ListPage = Page[GenreRead]
list_pagination = Depends(pagination_ctx(ListPage))


@router.get("/", dependencies=[list_pagination])
def list_genres() -> ListPage:
    with SessionLocal() as session:
        return paginate_rows(session, Genre, GenreRead)


@router.get("/{entity_id}")
def get_genre(entity_id: int) -> GenreRead:
    with SessionLocal() as session:
        return GenreRead.model_validate(
            get_row_or_404(session, Genre, "genre", entity_id)
        )
