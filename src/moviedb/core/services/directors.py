from moviedb.core.repositories.directors import DirectorRepository
from moviedb.schemas.directors import DirectorRead

from .base import Service


class DirectorService(Service[DirectorRead]):
    def __init__(self, repository: DirectorRepository) -> None:
        super().__init__(repository, "director")
