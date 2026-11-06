from collections.abc import Collection

from pydantic import BaseModel

from moviedb.core.errors import NotFoundError
from moviedb.core.pagination import PageParams, PageResult
from moviedb.core.repositories.base import ReadRepository


class Service[ReadType: BaseModel]:
    """Business logic shared by entities; talks only to a repository."""

    def __init__(self, repository: ReadRepository[ReadType], entity_name: str) -> None:
        self._repository = repository
        self._entity_name = entity_name

    def list(self, params: PageParams) -> PageResult[ReadType]:
        return self._repository.list_page(params)

    def get(self, entity_id: int) -> ReadType:
        entity = self._repository.get(entity_id)
        if entity is None:
            raise NotFoundError(self._entity_name, entity_id)
        return entity

    def get_many(self, entity_ids: Collection[int]) -> dict[int, ReadType]:
        return self._repository.get_many(entity_ids)
