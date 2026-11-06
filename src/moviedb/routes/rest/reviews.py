from fastapi import APIRouter
from fastapi_pagination import Page

from moviedb.dependencies import ReviewServiceDep
from moviedb.routes.rest.pagination import PageParamsDep, to_page
from moviedb.routes.rest.schemas.reviews import ReviewRead

router = APIRouter(prefix="/reviews", tags=["reviews"])

ListPage = Page[ReviewRead]


@router.get("/")
def list_reviews(service: ReviewServiceDep, params: PageParamsDep) -> ListPage:
    return to_page(ListPage, service.list(params), ReviewRead.from_domain)


@router.get("/{review_id}")
def get_review(review_id: int, service: ReviewServiceDep) -> ReviewRead:
    return ReviewRead.from_domain(service.get(review_id))
