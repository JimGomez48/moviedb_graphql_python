from moviedb.core.repositories.companies import CompanyRepository
from moviedb.schemas.companies import CompanyRead

from .base import Service


class CompanyService(Service[CompanyRead]):
    def __init__(self, repository: CompanyRepository) -> None:
        super().__init__(repository, "company")
