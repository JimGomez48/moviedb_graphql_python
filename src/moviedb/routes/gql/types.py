"""Strawberry types derived from the Pydantic read schemas (no ORM models here).

Scalar fields come from the schemas; relationships are resolved lazily through
per-request dataloaders so nested queries never issue one query per row.
"""

from typing import Annotated

import strawberry
from strawberry.experimental.pydantic import type as pydantic_type
from strawberry.types import Info

from moviedb.routes.gql.context import GraphQLContext
from moviedb.schemas.actors import ActorRead, CastMemberRead
from moviedb.schemas.companies import CompanyRead
from moviedb.schemas.directors import DirectorRead
from moviedb.schemas.genres import GenreRead
from moviedb.schemas.movies import MovieRead
from moviedb.schemas.mpaa_ratings import MpaaRatingRead
from moviedb.schemas.reviews import ReviewRead

type Ctx = Info[GraphQLContext, None]

# MovieType is defined last because it references every other type; the other
# types point back at it lazily.
MovieTypeRef = Annotated["MovieType", strawberry.lazy(__name__)]


@pydantic_type(model=MpaaRatingRead, all_fields=True)
class MpaaRatingType:
    id: strawberry.auto

    @strawberry.field
    async def movies(self, info: Ctx) -> list[MovieTypeRef]:
        movies = await info.context.loaders.movies_by_mpaa_rating.load(self.id)
        return [MovieType.from_pydantic(movie) for movie in movies]


@pydantic_type(model=GenreRead, all_fields=True)
class GenreType:
    id: strawberry.auto

    @strawberry.field
    async def movies(self, info: Ctx) -> list[MovieTypeRef]:
        movies = await info.context.loaders.movies_by_genre.load(self.id)
        return [MovieType.from_pydantic(movie) for movie in movies]


@pydantic_type(model=CompanyRead, all_fields=True)
class CompanyType:
    id: strawberry.auto

    @strawberry.field
    async def movies(self, info: Ctx) -> list[MovieTypeRef]:
        movies = await info.context.loaders.movies_by_company.load(self.id)
        return [MovieType.from_pydantic(movie) for movie in movies]


@pydantic_type(model=DirectorRead, all_fields=True)
class DirectorType:
    id: strawberry.auto

    @strawberry.field
    async def movies(self, info: Ctx) -> list[MovieTypeRef]:
        movies = await info.context.loaders.movies_by_director.load(self.id)
        return [MovieType.from_pydantic(movie) for movie in movies]


@pydantic_type(model=ActorRead, all_fields=True)
class ActorType:
    id: strawberry.auto

    @strawberry.field
    async def movies(self, info: Ctx) -> list[MovieTypeRef]:
        movies = await info.context.loaders.movies_by_actor.load(self.id)
        return [MovieType.from_pydantic(movie) for movie in movies]


@pydantic_type(model=CastMemberRead, all_fields=True)
class CastMemberType:
    pass


@pydantic_type(model=ReviewRead, all_fields=True)
class ReviewType:
    movie_id: strawberry.auto

    @strawberry.field
    async def movie(self, info: Ctx) -> MovieTypeRef | None:
        movie = await info.context.loaders.movie.load(self.movie_id)
        return None if movie is None else MovieType.from_pydantic(movie)


@pydantic_type(model=MovieRead, all_fields=True)
class MovieType:
    id: strawberry.auto
    mpaa_rating_id: strawberry.auto

    @strawberry.field
    async def mpaa_rating(self, info: Ctx) -> MpaaRatingType | None:
        if self.mpaa_rating_id is None:
            return None
        rating = await info.context.loaders.mpaa_rating.load(self.mpaa_rating_id)
        return None if rating is None else MpaaRatingType.from_pydantic(rating)

    @strawberry.field
    async def reviews(self, info: Ctx) -> list[ReviewType]:
        reviews = await info.context.loaders.reviews_by_movie.load(self.id)
        return [ReviewType.from_pydantic(review) for review in reviews]

    @strawberry.field
    async def cast(self, info: Ctx) -> list[CastMemberType]:
        cast = await info.context.loaders.cast_by_movie.load(self.id)
        return [CastMemberType.from_pydantic(member) for member in cast]

    @strawberry.field
    async def directors(self, info: Ctx) -> list[DirectorType]:
        directors = await info.context.loaders.directors_by_movie.load(self.id)
        return [DirectorType.from_pydantic(director) for director in directors]

    @strawberry.field
    async def genres(self, info: Ctx) -> list[GenreType]:
        genres = await info.context.loaders.genres_by_movie.load(self.id)
        return [GenreType.from_pydantic(genre) for genre in genres]

    @strawberry.field
    async def companies(self, info: Ctx) -> list[CompanyType]:
        companies = await info.context.loaders.companies_by_movie.load(self.id)
        return [CompanyType.from_pydantic(company) for company in companies]
