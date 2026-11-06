from collections.abc import Collection

from moviedb.core.repositories.directors import DirectorRepository
from moviedb.schemas.directors import DirectorRead

from .base import Service


class DirectorService(Service[DirectorRead]):
    def __init__(self, repository: DirectorRepository) -> None:
        super().__init__(repository, "director")
        self._related = repository

    def list_by_movie_ids(self, ids: Collection[int]) -> dict[int, list[DirectorRead]]:
        return self._related.list_by_movie_ids(ids)
