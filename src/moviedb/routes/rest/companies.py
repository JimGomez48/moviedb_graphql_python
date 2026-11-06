from fastapi import APIRouter, Depends
from fastapi_pagination import Page, pagination_ctx

from moviedb.dependencies import CompanyServiceDep
from moviedb.schemas.companies import CompanyRead

router = APIRouter(prefix="/companies", tags=["companies"])

ListPage = Page[CompanyRead]
list_pagination = Depends(pagination_ctx(ListPage))


@router.get("/", dependencies=[list_pagination])
def list_companies(service: CompanyServiceDep) -> ListPage:
    return service.list()


@router.get("/{company_id}")
def get_company(company_id: int, service: CompanyServiceDep) -> CompanyRead:
    return service.get(company_id)
