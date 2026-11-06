from collections.abc import Collection

from moviedb.core.domain.genres import Genre
from moviedb.core.repositories.genres import GenreRepository

from .base import Service


class GenreService(Service[Genre]):
    def __init__(self, repository: GenreRepository) -> None:
        super().__init__(repository, "genre")
        self._related = repository

    def list_by_movie_ids(self, ids: Collection[int]) -> dict[int, list[Genre]]:
        return self._related.list_by_movie_ids(ids)
