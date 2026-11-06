from collections.abc import Collection

from moviedb.core.repositories.companies import CompanyRepository
from moviedb.schemas.companies import CompanyRead

from .base import Service


class CompanyService(Service[CompanyRead]):
    def __init__(self, repository: CompanyRepository) -> None:
        super().__init__(repository, "company")
        self._related = repository

    def list_by_movie_ids(self, ids: Collection[int]) -> dict[int, list[CompanyRead]]:
        return self._related.list_by_movie_ids(ids)
