from collections.abc import Collection

from sqlalchemy.orm import Session

from moviedb.core.db.models import Director, MovieDirector
from moviedb.schemas.directors import DirectorCreate, DirectorRead

from .base import Repository


class DirectorRepository(Repository[Director, DirectorRead, DirectorCreate]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Director, DirectorRead)

    def list_by_movie_ids(
        self, movie_ids: Collection[int]
    ) -> dict[int, list[DirectorRead]]:
        return self._linked(
            MovieDirector.director_id, MovieDirector.movie_id, movie_ids
        )
