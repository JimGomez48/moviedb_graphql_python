from moviedb.core.repositories.reviews import ReviewRepository
from moviedb.schemas.reviews import ReviewRead

from .base import Service


class ReviewService(Service[ReviewRead]):
    def __init__(self, repository: ReviewRepository) -> None:
        super().__init__(repository, "review")
