from collections.abc import Collection

from moviedb.core.domain.movies import Movie, NewMovie
from moviedb.core.repositories.movies import MovieRepository

from .base import Service


class MovieService(Service[Movie]):
    def __init__(self, repository: MovieRepository) -> None:
        super().__init__(repository, "movie")
        self._movies = repository

    def create(self, data: NewMovie) -> Movie:
        return self._movies.create(data)

    def list_by_mpaa_rating_ids(self, ids: Collection[int]) -> dict[int, list[Movie]]:
        return self._movies.list_by_mpaa_rating_ids(ids)

    def list_by_actor_ids(self, ids: Collection[int]) -> dict[int, list[Movie]]:
        return self._movies.list_by_actor_ids(ids)

    def list_by_director_ids(self, ids: Collection[int]) -> dict[int, list[Movie]]:
        return self._movies.list_by_director_ids(ids)

    def list_by_genre_ids(self, ids: Collection[int]) -> dict[int, list[Movie]]:
        return self._movies.list_by_genre_ids(ids)

    def list_by_company_ids(self, ids: Collection[int]) -> dict[int, list[Movie]]:
        return self._movies.list_by_company_ids(ids)
