from fastapi import APIRouter
from fastapi_pagination import Page

from moviedb.dependencies import CompanyServiceDep
from moviedb.routes.rest.pagination import PageParamsDep, to_page
from moviedb.routes.rest.schemas.companies import CompanyRead

router = APIRouter(prefix="/companies", tags=["companies"])

ListPage = Page[CompanyRead]


@router.get("/")
def list_companies(service: CompanyServiceDep, params: PageParamsDep) -> ListPage:
    return to_page(ListPage, service.list(params), CompanyRead.from_domain)


@router.get("/{company_id}")
def get_company(company_id: int, service: CompanyServiceDep) -> CompanyRead:
    return CompanyRead.from_domain(service.get(company_id))
