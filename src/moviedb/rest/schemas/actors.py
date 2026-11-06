from pydantic import BaseModel

from moviedb.core.domain.actors import Actor, NewActor


class ActorBase(BaseModel):
    first_name: str
    last_name: str


class ActorCreate(ActorBase):
    def to_domain(self) -> NewActor:
        return NewActor(
            first_name=self.first_name,
            last_name=self.last_name,
        )


class ActorRead(ActorBase):
    id: int

    @classmethod
    def from_domain(cls, domain: Actor) -> ActorRead:
        return cls(
            id=domain.id,
            first_name=domain.first_name,
            last_name=domain.last_name,
        )
