"""Strawberry types for the GraphQL transport, mapped from core domain models.

Scalar fields are declared here, independently of REST and of the ORM.
Relationships are resolved lazily through per-request dataloaders, so nested
queries never issue one query per row.
"""

from typing import Annotated

import strawberry
from strawberry.types import Info

from moviedb.core.domain.actors import Actor, CastMember
from moviedb.core.domain.companies import Company
from moviedb.core.domain.directors import Director
from moviedb.core.domain.genres import Genre
from moviedb.core.domain.movies import Movie
from moviedb.core.domain.mpaa_ratings import MpaaRating
from moviedb.core.domain.reviews import Review
from moviedb.routes.gql.context import GraphQLContext

type Ctx = Info[GraphQLContext, None]

# MovieType is defined last because it references every other type; the other
# types point back at it lazily.
MovieTypeRef = Annotated["MovieType", strawberry.lazy(__name__)]


@strawberry.type
class MpaaRatingType:
    id: int
    code: str
    description: str | None

    @classmethod
    def from_domain(cls, domain: MpaaRating) -> MpaaRatingType:
        return cls(id=domain.id, code=domain.code, description=domain.description)

    @strawberry.field
    async def movies(self, info: Ctx) -> list[MovieTypeRef]:
        movies = await info.context.loaders.movies_by_mpaa_rating.load(self.id)
        return [MovieType.from_domain(movie) for movie in movies]


@strawberry.type
class GenreType:
    id: int
    name: str

    @classmethod
    def from_domain(cls, domain: Genre) -> GenreType:
        return cls(id=domain.id, name=domain.name)

    @strawberry.field
    async def movies(self, info: Ctx) -> list[MovieTypeRef]:
        movies = await info.context.loaders.movies_by_genre.load(self.id)
        return [MovieType.from_domain(movie) for movie in movies]


@strawberry.type
class CompanyType:
    id: int
    name: str

    @classmethod
    def from_domain(cls, domain: Company) -> CompanyType:
        return cls(id=domain.id, name=domain.name)

    @strawberry.field
    async def movies(self, info: Ctx) -> list[MovieTypeRef]:
        movies = await info.context.loaders.movies_by_company.load(self.id)
        return [MovieType.from_domain(movie) for movie in movies]


@strawberry.type
class DirectorType:
    id: int
    first_name: str
    last_name: str

    @classmethod
    def from_domain(cls, domain: Director) -> DirectorType:
        return cls(
            id=domain.id, first_name=domain.first_name, last_name=domain.last_name
        )

    @strawberry.field
    async def movies(self, info: Ctx) -> list[MovieTypeRef]:
        movies = await info.context.loaders.movies_by_director.load(self.id)
        return [MovieType.from_domain(movie) for movie in movies]


@strawberry.type
class ActorType:
    id: int
    first_name: str
    last_name: str

    @classmethod
    def from_domain(cls, domain: Actor) -> ActorType:
        return cls(
            id=domain.id, first_name=domain.first_name, last_name=domain.last_name
        )

    @strawberry.field
    async def movies(self, info: Ctx) -> list[MovieTypeRef]:
        movies = await info.context.loaders.movies_by_actor.load(self.id)
        return [MovieType.from_domain(movie) for movie in movies]


@strawberry.type
class CastMemberType:
    actor: ActorType
    roles: list[str]

    @classmethod
    def from_domain(cls, domain: CastMember) -> CastMemberType:
        return cls(actor=ActorType.from_domain(domain.actor), roles=list(domain.roles))


@strawberry.type
class ReviewType:
    id: int
    movie_id: int
    reviewer: str | None
    rating: int | None
    body: str | None

    @classmethod
    def from_domain(cls, domain: Review) -> ReviewType:
        return cls(
            id=domain.id,
            movie_id=domain.movie_id,
            reviewer=domain.reviewer,
            rating=domain.rating,
            body=domain.body,
        )

    @strawberry.field
    async def movie(self, info: Ctx) -> MovieTypeRef | None:
        movie = await info.context.loaders.movie.load(self.movie_id)
        return None if movie is None else MovieType.from_domain(movie)


@strawberry.type
class MovieType:
    id: int
    title: str
    release_year: int | None
    mpaa_rating_id: int | None

    @classmethod
    def from_domain(cls, domain: Movie) -> MovieType:
        return cls(
            id=domain.id,
            title=domain.title,
            release_year=domain.release_year,
            mpaa_rating_id=domain.mpaa_rating_id,
        )

    @strawberry.field
    async def mpaa_rating(self, info: Ctx) -> MpaaRatingType | None:
        if self.mpaa_rating_id is None:
            return None
        rating = await info.context.loaders.mpaa_rating.load(self.mpaa_rating_id)
        return None if rating is None else MpaaRatingType.from_domain(rating)

    @strawberry.field
    async def reviews(self, info: Ctx) -> list[ReviewType]:
        reviews = await info.context.loaders.reviews_by_movie.load(self.id)
        return [ReviewType.from_domain(review) for review in reviews]

    @strawberry.field
    async def cast(self, info: Ctx) -> list[CastMemberType]:
        cast = await info.context.loaders.cast_by_movie.load(self.id)
        return [CastMemberType.from_domain(member) for member in cast]

    @strawberry.field
    async def directors(self, info: Ctx) -> list[DirectorType]:
        directors = await info.context.loaders.directors_by_movie.load(self.id)
        return [DirectorType.from_domain(director) for director in directors]

    @strawberry.field
    async def genres(self, info: Ctx) -> list[GenreType]:
        genres = await info.context.loaders.genres_by_movie.load(self.id)
        return [GenreType.from_domain(genre) for genre in genres]

    @strawberry.field
    async def companies(self, info: Ctx) -> list[CompanyType]:
        companies = await info.context.loaders.companies_by_movie.load(self.id)
        return [CompanyType.from_domain(company) for company in companies]
