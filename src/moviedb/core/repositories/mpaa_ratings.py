from sqlalchemy.orm import Session

from moviedb.core.db.models import MpaaRating
from moviedb.schemas.mpaa_ratings import MpaaRatingCreate, MpaaRatingRead

from .base import Repository


class MpaaRatingRepository(Repository[MpaaRating, MpaaRatingRead, MpaaRatingCreate]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, MpaaRating, MpaaRatingRead)
