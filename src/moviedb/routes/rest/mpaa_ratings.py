from fastapi import APIRouter, Depends
from fastapi_pagination import Page, pagination_ctx

from moviedb.dependencies import MpaaRatingServiceDep
from moviedb.schemas.mpaa_ratings import MpaaRatingRead

router = APIRouter(prefix="/mpaa-ratings", tags=["mpaa-ratings"])

ListPage = Page[MpaaRatingRead]
list_pagination = Depends(pagination_ctx(ListPage))


@router.get("/", dependencies=[list_pagination])
def list_mpaa_ratings(service: MpaaRatingServiceDep) -> ListPage:
    return service.list()


@router.get("/{mpaa_rating_id}")
def get_mpaa_rating(
    mpaa_rating_id: int, service: MpaaRatingServiceDep
) -> MpaaRatingRead:
    return service.get(mpaa_rating_id)
