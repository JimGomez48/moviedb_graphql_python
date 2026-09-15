from pydantic import BaseModel, ConfigDict


class DirectorBase(BaseModel):
    first_name: str
    last_name: str


class DirectorCreate(DirectorBase):
    pass


class DirectorRead(DirectorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
