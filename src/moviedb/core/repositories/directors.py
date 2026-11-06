from collections.abc import Collection

from sqlalchemy.orm import Session

from moviedb.core.db import models
from moviedb.core.domain.directors import Director, NewDirector

from .base import Repository


def _to_director(row: models.Director) -> Director:
    return Director(
        id=row.id,
        first_name=row.first_name,
        last_name=row.last_name,
    )


class DirectorRepository(Repository[models.Director, Director, NewDirector]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, models.Director, _to_director)

    def list_by_movie_ids(
        self, movie_ids: Collection[int]
    ) -> dict[int, list[Director]]:
        return self._linked(
            models.MovieDirector.director_id, models.MovieDirector.movie_id, movie_ids
        )
