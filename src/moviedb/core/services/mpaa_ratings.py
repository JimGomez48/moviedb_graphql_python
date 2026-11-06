from moviedb.core.repositories.mpaa_ratings import MpaaRatingRepository
from moviedb.schemas.mpaa_ratings import MpaaRatingRead

from .base import Service


class MpaaRatingService(Service[MpaaRatingRead]):
    def __init__(self, repository: MpaaRatingRepository) -> None:
        super().__init__(repository, "mpaa_rating")
