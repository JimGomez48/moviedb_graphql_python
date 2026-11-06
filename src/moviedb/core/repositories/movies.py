from collections.abc import Collection

from sqlalchemy.orm import Session

from moviedb.core.db import models
from moviedb.core.domain.movies import Movie, NewMovie

from .base import Repository


def _to_movie(row: models.Movie) -> Movie:
    return Movie(
        id=row.id,
        title=row.title,
        release_year=row.release_year,
        mpaa_rating_id=row.mpaa_rating_id,
    )


class MovieRepository(Repository[models.Movie, Movie, NewMovie]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, models.Movie, _to_movie)

    def list_by_mpaa_rating_ids(
        self, rating_ids: Collection[int]
    ) -> dict[int, list[Movie]]:
        return self._grouped_by(models.Movie.mpaa_rating_id, rating_ids)

    def list_by_actor_ids(self, actor_ids: Collection[int]) -> dict[int, list[Movie]]:
        return self._linked(
            models.MovieActor.movie_id, models.MovieActor.actor_id, actor_ids
        )

    def list_by_director_ids(
        self, director_ids: Collection[int]
    ) -> dict[int, list[Movie]]:
        return self._linked(
            models.MovieDirector.movie_id,
            models.MovieDirector.director_id,
            director_ids,
        )

    def list_by_genre_ids(self, genre_ids: Collection[int]) -> dict[int, list[Movie]]:
        return self._linked(
            models.MovieGenre.movie_id, models.MovieGenre.genre_id, genre_ids
        )

    def list_by_company_ids(
        self, company_ids: Collection[int]
    ) -> dict[int, list[Movie]]:
        return self._linked(
            models.MovieCompany.movie_id, models.MovieCompany.company_id, company_ids
        )
