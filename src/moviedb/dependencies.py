"""Composition root: wires sessions, repositories and services for routers.

This is the only place between the HTTP layer and the database, so routers and
services never import `moviedb.core.db` themselves.
"""

from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from moviedb.core.db.conn import SessionLocal
from moviedb.core.repositories.actors import ActorRepository
from moviedb.core.repositories.companies import CompanyRepository
from moviedb.core.repositories.directors import DirectorRepository
from moviedb.core.repositories.genres import GenreRepository
from moviedb.core.repositories.movies import MovieRepository
from moviedb.core.repositories.mpaa_ratings import MpaaRatingRepository
from moviedb.core.repositories.reviews import ReviewRepository
from moviedb.core.services.actors import ActorService
from moviedb.core.services.companies import CompanyService
from moviedb.core.services.directors import DirectorService
from moviedb.core.services.genres import GenreService
from moviedb.core.services.movies import MovieService
from moviedb.core.services.mpaa_ratings import MpaaRatingService
from moviedb.core.services.reviews import ReviewService


def get_db_session() -> Iterator[Session]:
    with SessionLocal() as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db_session)]


def get_actor_service(session: SessionDep) -> ActorService:
    return ActorService(ActorRepository(session))


ActorServiceDep = Annotated[ActorService, Depends(get_actor_service)]


def get_movie_service(session: SessionDep) -> MovieService:
    return MovieService(MovieRepository(session))


MovieServiceDep = Annotated[MovieService, Depends(get_movie_service)]


def get_director_service(session: SessionDep) -> DirectorService:
    return DirectorService(DirectorRepository(session))


DirectorServiceDep = Annotated[DirectorService, Depends(get_director_service)]


def get_mpaa_rating_service(session: SessionDep) -> MpaaRatingService:
    return MpaaRatingService(MpaaRatingRepository(session))


MpaaRatingServiceDep = Annotated[MpaaRatingService, Depends(get_mpaa_rating_service)]


def get_genre_service(session: SessionDep) -> GenreService:
    return GenreService(GenreRepository(session))


GenreServiceDep = Annotated[GenreService, Depends(get_genre_service)]


def get_company_service(session: SessionDep) -> CompanyService:
    return CompanyService(CompanyRepository(session))


CompanyServiceDep = Annotated[CompanyService, Depends(get_company_service)]


def get_review_service(session: SessionDep) -> ReviewService:
    return ReviewService(ReviewRepository(session))


ReviewServiceDep = Annotated[ReviewService, Depends(get_review_service)]
