from collections.abc import Collection

from moviedb.core.domain.reviews import Review
from moviedb.core.repositories.reviews import ReviewRepository

from .base import Service


class ReviewService(Service[Review]):
    def __init__(self, repository: ReviewRepository) -> None:
        super().__init__(repository, "review")
        self._related = repository

    def list_by_movie_ids(self, ids: Collection[int]) -> dict[int, list[Review]]:
        return self._related.list_by_movie_ids(ids)
