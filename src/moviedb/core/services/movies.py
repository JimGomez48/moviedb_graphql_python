from collections.abc import Collection

from moviedb.core.repositories.movies import MovieRepository
from moviedb.schemas.movies import MovieCreate, MovieRead

from .base import Service


class MovieService(Service[MovieRead]):
    def __init__(self, repository: MovieRepository) -> None:
        super().__init__(repository, "movie")
        self._movies = repository

    def create(self, data: MovieCreate) -> MovieRead:
        return self._movies.create(data)

    def list_by_mpaa_rating_ids(
        self, ids: Collection[int]
    ) -> dict[int, list[MovieRead]]:
        return self._movies.list_by_mpaa_rating_ids(ids)

    def list_by_actor_ids(self, ids: Collection[int]) -> dict[int, list[MovieRead]]:
        return self._movies.list_by_actor_ids(ids)

    def list_by_director_ids(self, ids: Collection[int]) -> dict[int, list[MovieRead]]:
        return self._movies.list_by_director_ids(ids)

    def list_by_genre_ids(self, ids: Collection[int]) -> dict[int, list[MovieRead]]:
        return self._movies.list_by_genre_ids(ids)

    def list_by_company_ids(self, ids: Collection[int]) -> dict[int, list[MovieRead]]:
        return self._movies.list_by_company_ids(ids)
