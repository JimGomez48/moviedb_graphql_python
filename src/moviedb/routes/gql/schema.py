"""GraphQL root query: every resolver calls a service, never the database."""

from collections.abc import Callable

import strawberry
from pydantic import BaseModel
from strawberry.types import Info

from moviedb.core.errors import NotFoundError
from moviedb.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE, PageParams
from moviedb.routes.gql.context import GraphQLContext
from moviedb.routes.gql.types import (
    ActorType,
    CompanyType,
    DirectorType,
    GenreType,
    MovieType,
    MpaaRatingType,
    ReviewType,
)

type Ctx = Info[GraphQLContext, None]


def _page_params(page: int, size: int) -> PageParams:
    if page < 1:
        raise ValueError("page must be at least 1")
    if not 1 <= size <= MAX_PAGE_SIZE:
        raise ValueError(f"size must be between 1 and {MAX_PAGE_SIZE}")
    return PageParams(page=page, size=size)


def _get_or_none[T: BaseModel](fetch: Callable[[int], T], entity_id: int) -> T | None:
    try:
        return fetch(entity_id)
    except NotFoundError:
        return None


@strawberry.type
class Query:
    @strawberry.field
    def actors(
        self, info: Ctx, page: int = 1, size: int = DEFAULT_PAGE_SIZE
    ) -> list[ActorType]:
        result = info.context.actors.list(_page_params(page, size))
        return [ActorType.from_pydantic(item) for item in result.items]

    @strawberry.field
    def actor(self, info: Ctx, id: int) -> ActorType | None:
        found = _get_or_none(info.context.actors.get, id)
        return None if found is None else ActorType.from_pydantic(found)

    @strawberry.field
    def directors(
        self, info: Ctx, page: int = 1, size: int = DEFAULT_PAGE_SIZE
    ) -> list[DirectorType]:
        result = info.context.directors.list(_page_params(page, size))
        return [DirectorType.from_pydantic(item) for item in result.items]

    @strawberry.field
    def director(self, info: Ctx, id: int) -> DirectorType | None:
        found = _get_or_none(info.context.directors.get, id)
        return None if found is None else DirectorType.from_pydantic(found)

    @strawberry.field
    def mpaa_ratings(
        self, info: Ctx, page: int = 1, size: int = DEFAULT_PAGE_SIZE
    ) -> list[MpaaRatingType]:
        result = info.context.mpaa_ratings.list(_page_params(page, size))
        return [MpaaRatingType.from_pydantic(item) for item in result.items]

    @strawberry.field
    def mpaa_rating(self, info: Ctx, id: int) -> MpaaRatingType | None:
        found = _get_or_none(info.context.mpaa_ratings.get, id)
        return None if found is None else MpaaRatingType.from_pydantic(found)

    @strawberry.field
    def genres(
        self, info: Ctx, page: int = 1, size: int = DEFAULT_PAGE_SIZE
    ) -> list[GenreType]:
        result = info.context.genres.list(_page_params(page, size))
        return [GenreType.from_pydantic(item) for item in result.items]

    @strawberry.field
    def genre(self, info: Ctx, id: int) -> GenreType | None:
        found = _get_or_none(info.context.genres.get, id)
        return None if found is None else GenreType.from_pydantic(found)

    @strawberry.field
    def companies(
        self, info: Ctx, page: int = 1, size: int = DEFAULT_PAGE_SIZE
    ) -> list[CompanyType]:
        result = info.context.companies.list(_page_params(page, size))
        return [CompanyType.from_pydantic(item) for item in result.items]

    @strawberry.field
    def company(self, info: Ctx, id: int) -> CompanyType | None:
        found = _get_or_none(info.context.companies.get, id)
        return None if found is None else CompanyType.from_pydantic(found)

    @strawberry.field
    def movies(
        self, info: Ctx, page: int = 1, size: int = DEFAULT_PAGE_SIZE
    ) -> list[MovieType]:
        result = info.context.movies.list(_page_params(page, size))
        return [MovieType.from_pydantic(item) for item in result.items]

    @strawberry.field
    def movie(self, info: Ctx, id: int) -> MovieType | None:
        found = _get_or_none(info.context.movies.get, id)
        return None if found is None else MovieType.from_pydantic(found)

    @strawberry.field
    def reviews(
        self, info: Ctx, page: int = 1, size: int = DEFAULT_PAGE_SIZE
    ) -> list[ReviewType]:
        result = info.context.reviews.list(_page_params(page, size))
        return [ReviewType.from_pydantic(item) for item in result.items]

    @strawberry.field
    def review(self, info: Ctx, id: int) -> ReviewType | None:
        found = _get_or_none(info.context.reviews.get, id)
        return None if found is None else ReviewType.from_pydantic(found)


schema = strawberry.Schema(query=Query)
