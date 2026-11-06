from moviedb.core.repositories.genres import GenreRepository
from moviedb.schemas.genres import GenreRead

from .base import Service


class GenreService(Service[GenreRead]):
    def __init__(self, repository: GenreRepository) -> None:
        super().__init__(repository, "genre")
