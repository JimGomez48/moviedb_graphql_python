from moviedb.core.repositories.actors import ActorRepository
from moviedb.schemas.actors import ActorCreate, ActorRead

from .base import Service


class ActorService(Service[ActorRead]):
    def __init__(self, repository: ActorRepository) -> None:
        super().__init__(repository, "actor")
        self._actors = repository

    def create(self, data: ActorCreate) -> ActorRead:
        return self._actors.create(data)
