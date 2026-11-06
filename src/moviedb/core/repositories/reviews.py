from collections.abc import Collection

from sqlalchemy.orm import Session

from moviedb.core.db import models
from moviedb.core.domain.reviews import NewReview, Review

from .base import Repository


def _to_review(row: models.Review) -> Review:
    return Review(
        id=row.id,
        movie_id=row.movie_id,
        reviewer=row.reviewer,
        rating=row.rating,
        body=row.body,
    )


class ReviewRepository(Repository[models.Review, Review, NewReview]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, models.Review, _to_review)

    def list_by_movie_ids(self, movie_ids: Collection[int]) -> dict[int, list[Review]]:
        return self._grouped_by(models.Review.movie_id, movie_ids)
