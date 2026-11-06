from pydantic import BaseModel

from moviedb.core.domain.companies import Company, NewCompany


class CompanyBase(BaseModel):
    name: str


class CompanyCreate(CompanyBase):
    def to_domain(self) -> NewCompany:
        return NewCompany(
            name=self.name,
        )


class CompanyRead(CompanyBase):
    id: int

    @classmethod
    def from_domain(cls, domain: Company) -> CompanyRead:
        return cls(
            id=domain.id,
            name=domain.name,
        )
