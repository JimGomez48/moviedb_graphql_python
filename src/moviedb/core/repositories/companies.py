from collections.abc import Collection

from sqlalchemy.orm import Session

from moviedb.core.db import models
from moviedb.core.domain.companies import Company, NewCompany

from .base import Repository


def _to_company(row: models.Company) -> Company:
    return Company(
        id=row.id,
        name=row.name,
    )


class CompanyRepository(Repository[models.Company, Company, NewCompany]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, models.Company, _to_company)

    def list_by_movie_ids(self, movie_ids: Collection[int]) -> dict[int, list[Company]]:
        return self._linked(
            models.MovieCompany.company_id, models.MovieCompany.movie_id, movie_ids
        )
