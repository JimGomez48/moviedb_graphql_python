"""Per-request GraphQL context built from the same services REST uses."""

from dataclasses import dataclass

from strawberry.fastapi import BaseContext

from moviedb.core.services.actors import ActorService
from moviedb.core.services.companies import CompanyService
from moviedb.core.services.directors import DirectorService
from moviedb.core.services.genres import GenreService
from moviedb.core.services.movies import MovieService
from moviedb.core.services.mpaa_ratings import MpaaRatingService
from moviedb.core.services.reviews import ReviewService
from moviedb.dependencies import (
    ActorServiceDep,
    CompanyServiceDep,
    DirectorServiceDep,
    GenreServiceDep,
    MovieServiceDep,
    MpaaRatingServiceDep,
    ReviewServiceDep,
)

from .loaders import Loaders


@dataclass
class GraphQLContext(BaseContext):
    actors: ActorService
    companies: CompanyService
    directors: DirectorService
    genres: GenreService
    movies: MovieService
    mpaa_ratings: MpaaRatingService
    reviews: ReviewService
    loaders: Loaders


def get_graphql_context(
    actors: ActorServiceDep,
    companies: CompanyServiceDep,
    directors: DirectorServiceDep,
    genres: GenreServiceDep,
    movies: MovieServiceDep,
    mpaa_ratings: MpaaRatingServiceDep,
    reviews: ReviewServiceDep,
) -> GraphQLContext:
    return GraphQLContext(
        actors=actors,
        companies=companies,
        directors=directors,
        genres=genres,
        movies=movies,
        mpaa_ratings=mpaa_ratings,
        reviews=reviews,
        loaders=Loaders(
            actors=actors,
            companies=companies,
            directors=directors,
            genres=genres,
            movies=movies,
            mpaa_ratings=mpaa_ratings,
            reviews=reviews,
        ),
    )
