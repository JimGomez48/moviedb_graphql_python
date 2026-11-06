from collections.abc import Collection

from moviedb.core.domain.actors import Actor, CastMember, NewActor
from moviedb.core.repositories.actors import ActorRepository

from .base import Service


class ActorService(Service[Actor]):
    def __init__(self, repository: ActorRepository) -> None:
        super().__init__(repository, "actor")
        self._actors = repository

    def create(self, data: NewActor) -> Actor:
        return self._actors.create(data)

    def cast_by_movie_ids(self, ids: Collection[int]) -> dict[int, list[CastMember]]:
        return self._actors.cast_by_movie_ids(ids)
