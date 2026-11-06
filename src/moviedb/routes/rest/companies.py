from fastapi import APIRouter
from fastapi_pagination import Page

from moviedb.dependencies import CompanyServiceDep
from moviedb.routes.rest.pagination import PageParamsDep, to_page
from moviedb.schemas.companies import CompanyRead

router = APIRouter(prefix="/companies", tags=["companies"])

ListPage = Page[CompanyRead]


@router.get("/")
def list_companies(service: CompanyServiceDep, params: PageParamsDep) -> ListPage:
    return to_page(ListPage, service.list(params))


@router.get("/{company_id}")
def get_company(company_id: int, service: CompanyServiceDep) -> CompanyRead:
    return service.get(company_id)
