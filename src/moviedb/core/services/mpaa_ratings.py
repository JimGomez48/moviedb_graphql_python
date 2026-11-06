from moviedb.core.domain.mpaa_ratings import MpaaRating
from moviedb.core.repositories.mpaa_ratings import MpaaRatingRepository

from .base import Service


class MpaaRatingService(Service[MpaaRating]):
    def __init__(self, repository: MpaaRatingRepository) -> None:
        super().__init__(repository, "mpaa_rating")
