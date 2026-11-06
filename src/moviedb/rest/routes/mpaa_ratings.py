from fastapi import APIRouter
from fastapi_pagination import Page

from moviedb.dependencies import MpaaRatingServiceDep
from moviedb.rest.pagination import PageParamsDep, to_page
from moviedb.rest.schemas.mpaa_ratings import MpaaRatingRead

router = APIRouter(prefix="/mpaa-ratings", tags=["mpaa-ratings"])

ListPage = Page[MpaaRatingRead]


@router.get("/")
def list_mpaa_ratings(service: MpaaRatingServiceDep, params: PageParamsDep) -> ListPage:
    return to_page(ListPage, service.list(params), MpaaRatingRead.from_domain)


@router.get("/{mpaa_rating_id}")
def get_mpaa_rating(
    mpaa_rating_id: int, service: MpaaRatingServiceDep
) -> MpaaRatingRead:
    return MpaaRatingRead.from_domain(service.get(mpaa_rating_id))
