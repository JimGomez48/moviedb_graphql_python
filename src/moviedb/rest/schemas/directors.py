from pydantic import BaseModel

from moviedb.core.domain.directors import Director, NewDirector


class DirectorBase(BaseModel):
    first_name: str
    last_name: str


class DirectorCreate(DirectorBase):
    def to_domain(self) -> NewDirector:
        return NewDirector(
            first_name=self.first_name,
            last_name=self.last_name,
        )


class DirectorRead(DirectorBase):
    id: int

    @classmethod
    def from_domain(cls, domain: Director) -> DirectorRead:
        return cls(
            id=domain.id,
            first_name=domain.first_name,
            last_name=domain.last_name,
        )
