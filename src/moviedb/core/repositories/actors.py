from collections.abc import Collection

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, selectinload

from moviedb.core.db.models import Actor, MovieActor
from moviedb.schemas.actors import ActorCreate, ActorRead, CastMemberRead

from .base import Repository


class ActorRepository(Repository[Actor, ActorRead, ActorCreate]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Actor, ActorRead)

    def cast_by_movie_ids(
        self, movie_ids: Collection[int]
    ) -> dict[int, list[CastMemberRead]]:
        if not movie_ids:
            return {}
        credits = self._session.scalars(
            select(MovieActor)
            .where(MovieActor.movie_id.in_(movie_ids))
            .options(joinedload(MovieActor.actor), selectinload(MovieActor.roles))
            .order_by(MovieActor.id)
        )
        cast: dict[int, list[CastMemberRead]] = {}
        for credit in credits:
            cast.setdefault(credit.movie_id, []).append(
                CastMemberRead(
                    actor=ActorRead.model_validate(credit.actor),
                    roles=[
                        role.role for role in sorted(credit.roles, key=lambda r: r.id)
                    ],
                )
            )
        return cast
