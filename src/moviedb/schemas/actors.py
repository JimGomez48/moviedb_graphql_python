from pydantic import BaseModel, ConfigDict


class ActorBase(BaseModel):
    first_name: str
    last_name: str


class ActorCreate(ActorBase):
    pass


class ActorRead(ActorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class CastMemberRead(BaseModel):
    """An actor's participation in one movie, with the roles they played."""

    actor: ActorRead
    roles: list[str]
