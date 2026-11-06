from collections.abc import Collection

from sqlalchemy.orm import Session

from moviedb.core.db.models import Genre, MovieGenre
from moviedb.schemas.genres import GenreCreate, GenreRead

from .base import Repository


class GenreRepository(Repository[Genre, GenreRead, GenreCreate]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Genre, GenreRead)

    def list_by_movie_ids(
        self, movie_ids: Collection[int]
    ) -> dict[int, list[GenreRead]]:
        return self._linked(MovieGenre.genre_id, MovieGenre.movie_id, movie_ids)
