from sqlalchemy.orm import Session

from moviedb.core.db.models import Actor
from moviedb.schemas.actors import ActorCreate, ActorRead

from .base import Repository


class ActorRepository(Repository[Actor, ActorRead, ActorCreate]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Actor, ActorRead)
