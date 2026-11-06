from sqlalchemy.orm import Session

from moviedb.core.db.models import Company
from moviedb.schemas.companies import CompanyCreate, CompanyRead

from .base import Repository


class CompanyRepository(Repository[Company, CompanyRead, CompanyCreate]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Company, CompanyRead)
