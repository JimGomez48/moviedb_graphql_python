from sqlalchemy.orm import Session

from moviedb.core.db.models import Review
from moviedb.schemas.reviews import ReviewCreate, ReviewRead

from .base import Repository


class ReviewRepository(Repository[Review, ReviewRead, ReviewCreate]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Review, ReviewRead)
