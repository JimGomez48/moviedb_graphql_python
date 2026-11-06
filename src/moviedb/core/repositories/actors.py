from collections.abc import Collection

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, selectinload

from moviedb.core.db import models
from moviedb.core.domain.actors import Actor, CastMember, NewActor

from .base import Repository


def _to_actor(row: models.Actor) -> Actor:
    return Actor(
        id=row.id,
        first_name=row.first_name,
        last_name=row.last_name,
    )


class ActorRepository(Repository[models.Actor, Actor, NewActor]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, models.Actor, _to_actor)

    def cast_by_movie_ids(
        self, movie_ids: Collection[int]
    ) -> dict[int, list[CastMember]]:
        if not movie_ids:
            return {}
        credits = self._session.scalars(
            select(models.MovieActor)
            .where(models.MovieActor.movie_id.in_(movie_ids))
            .options(
                joinedload(models.MovieActor.actor),
                selectinload(models.MovieActor.roles),
            )
            .order_by(models.MovieActor.id)
        )
        cast: dict[int, list[CastMember]] = {}
        for credit in credits:
            roles = sorted(credit.roles, key=lambda role: role.id)
            cast.setdefault(credit.movie_id, []).append(
                CastMember(
                    actor=_to_actor(credit.actor),
                    roles=tuple(role.role for role in roles),
                )
            )
        return cast
