from collections.abc import Collection

from moviedb.core.repositories.actors import ActorRepository
from moviedb.schemas.actors import ActorCreate, ActorRead, CastMemberRead

from .base import Service


class ActorService(Service[ActorRead]):
    def __init__(self, repository: ActorRepository) -> None:
        super().__init__(repository, "actor")
        self._actors = repository

    def create(self, data: ActorCreate) -> ActorRead:
        return self._actors.create(data)

    def cast_by_movie_ids(
        self, ids: Collection[int]
    ) -> dict[int, list[CastMemberRead]]:
        return self._actors.cast_by_movie_ids(ids)
