from pydantic import BaseModel

from moviedb.core.domain.mpaa_ratings import MpaaRating, NewMpaaRating


class MpaaRatingBase(BaseModel):
    code: str
    description: str | None = None


class MpaaRatingCreate(MpaaRatingBase):
    def to_domain(self) -> NewMpaaRating:
        return NewMpaaRating(
            code=self.code,
            description=self.description,
        )


class MpaaRatingRead(MpaaRatingBase):
    id: int

    @classmethod
    def from_domain(cls, domain: MpaaRating) -> MpaaRatingRead:
        return cls(
            id=domain.id,
            code=domain.code,
            description=domain.description,
        )
