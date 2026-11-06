from fastapi import APIRouter, Depends
from fastapi_pagination import Page, pagination_ctx

from moviedb.dependencies import ReviewServiceDep
from moviedb.schemas.reviews import ReviewRead

router = APIRouter(prefix="/reviews", tags=["reviews"])

ListPage = Page[ReviewRead]
list_pagination = Depends(pagination_ctx(ListPage))


@router.get("/", dependencies=[list_pagination])
def list_reviews(service: ReviewServiceDep) -> ListPage:
    return service.list()


@router.get("/{review_id}")
def get_review(review_id: int, service: ReviewServiceDep) -> ReviewRead:
    return service.get(review_id)
