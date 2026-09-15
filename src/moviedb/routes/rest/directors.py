from fastapi import APIRouter, Depends
from fastapi_pagination import Page, pagination_ctx

from moviedb.core.db.conn import SessionLocal
from moviedb.core.db.models import Director
from moviedb.schemas.directors import DirectorRead

from .utils import get_row_or_404, paginate_rows

router = APIRouter(prefix="/directors", tags=["directors"])

ListPage = Page[DirectorRead]
list_pagination = Depends(pagination_ctx(ListPage))


@router.get("/", dependencies=[list_pagination])
def list_directors() -> ListPage:
    with SessionLocal() as session:
        return paginate_rows(session, Director, DirectorRead)


@router.get("/{entity_id}")
def get_director(entity_id: int) -> DirectorRead:
    with SessionLocal() as session:
        return DirectorRead.model_validate(
            get_row_or_404(session, Director, "director", entity_id)
        )
