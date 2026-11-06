from sqlalchemy.orm import Session

from moviedb.core.db import models
from moviedb.core.domain.mpaa_ratings import MpaaRating, NewMpaaRating

from .base import Repository


def _to_mpaa_rating(row: models.MpaaRating) -> MpaaRating:
    return MpaaRating(
        id=row.id,
        code=row.code,
        description=row.description,
    )


class MpaaRatingRepository(Repository[models.MpaaRating, MpaaRating, NewMpaaRating]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, models.MpaaRating, _to_mpaa_rating)
