from collections.abc import Collection

from sqlalchemy.orm import Session

from moviedb.core.db import models
from moviedb.core.domain.genres import Genre, NewGenre

from .base import Repository


def _to_genre(row: models.Genre) -> Genre:
    return Genre(
        id=row.id,
        name=row.name,
    )


class GenreRepository(Repository[models.Genre, Genre, NewGenre]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, models.Genre, _to_genre)

    def list_by_movie_ids(self, movie_ids: Collection[int]) -> dict[int, list[Genre]]:
        return self._linked(
            models.MovieGenre.genre_id, models.MovieGenre.movie_id, movie_ids
        )
