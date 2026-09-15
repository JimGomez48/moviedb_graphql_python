from fastapi import APIRouter, Depends
from fastapi_pagination import Page, pagination_ctx

from moviedb.core.db.conn import SessionLocal
from moviedb.core.db.models import Company
from moviedb.schemas.companies import CompanyRead

from .utils import get_row_or_404, paginate_rows

router = APIRouter(prefix="/companies", tags=["companies"])

ListPage = Page[CompanyRead]
list_pagination = Depends(pagination_ctx(ListPage))


@router.get("/", dependencies=[list_pagination])
def list_companies() -> ListPage:
    with SessionLocal() as session:
        return paginate_rows(session, Company, CompanyRead)


@router.get("/{entity_id}")
def get_company(entity_id: int) -> CompanyRead:
    with SessionLocal() as session:
        return CompanyRead.model_validate(
            get_row_or_404(session, Company, "company", entity_id)
        )
