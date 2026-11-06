from moviedb.core.repositories.movies import MovieRepository
from moviedb.schemas.movies import MovieCreate, MovieRead

from .base import Service


class MovieService(Service[MovieRead]):
    def __init__(self, repository: MovieRepository) -> None:
        super().__init__(repository, "movie")
        self._movies = repository

    def create(self, data: MovieCreate) -> MovieRead:
        return self._movies.create(data)
