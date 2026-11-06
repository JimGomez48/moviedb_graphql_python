from collections.abc import Collection

from sqlalchemy.orm import Session

from moviedb.core.db.models import Company, MovieCompany
from moviedb.schemas.companies import CompanyCreate, CompanyRead

from .base import Repository


class CompanyRepository(Repository[Company, CompanyRead, CompanyCreate]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Company, CompanyRead)

    def list_by_movie_ids(
        self, movie_ids: Collection[int]
    ) -> dict[int, list[CompanyRead]]:
        return self._linked(MovieCompany.company_id, MovieCompany.movie_id, movie_ids)
