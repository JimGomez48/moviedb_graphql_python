from pydantic import BaseModel, ConfigDict


class CompanyBase(BaseModel):
    name: str


class CompanyCreate(CompanyBase):
    pass


class CompanyRead(CompanyBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
