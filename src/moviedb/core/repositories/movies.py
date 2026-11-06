from collections.abc import Collection

from sqlalchemy.orm import Session

from moviedb.core.db.models import (
    Movie,
    MovieActor,
    MovieCompany,
    MovieDirector,
    MovieGenre,
)
from moviedb.schemas.movies import MovieCreate, MovieRead

from .base import Repository


class MovieRepository(Repository[Movie, MovieRead, MovieCreate]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Movie, MovieRead)

    def list_by_mpaa_rating_ids(
        self, rating_ids: Collection[int]
    ) -> dict[int, list[MovieRead]]:
        return self._grouped_by(Movie.mpaa_rating_id, rating_ids)

    def list_by_actor_ids(
        self, actor_ids: Collection[int]
    ) -> dict[int, list[MovieRead]]:
        return self._linked(MovieActor.movie_id, MovieActor.actor_id, actor_ids)

    def list_by_director_ids(
        self, director_ids: Collection[int]
    ) -> dict[int, list[MovieRead]]:
        return self._linked(
            MovieDirector.movie_id, MovieDirector.director_id, director_ids
        )

    def list_by_genre_ids(
        self, genre_ids: Collection[int]
    ) -> dict[int, list[MovieRead]]:
        return self._linked(MovieGenre.movie_id, MovieGenre.genre_id, genre_ids)

    def list_by_company_ids(
        self, company_ids: Collection[int]
    ) -> dict[int, list[MovieRead]]:
        return self._linked(MovieCompany.movie_id, MovieCompany.company_id, company_ids)
