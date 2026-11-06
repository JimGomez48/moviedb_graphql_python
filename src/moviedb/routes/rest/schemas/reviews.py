from pydantic import BaseModel

from moviedb.core.domain.reviews import NewReview, Review


class ReviewBase(BaseModel):
    movie_id: int
    reviewer: str | None = None
    rating: int | None = None
    body: str | None = None


class ReviewCreate(ReviewBase):
    def to_domain(self) -> NewReview:
        return NewReview(
            movie_id=self.movie_id,
            reviewer=self.reviewer,
            rating=self.rating,
            body=self.body,
        )


class ReviewRead(ReviewBase):
    id: int

    @classmethod
    def from_domain(cls, domain: Review) -> ReviewRead:
        return cls(
            id=domain.id,
            movie_id=domain.movie_id,
            reviewer=domain.reviewer,
            rating=domain.rating,
            body=domain.body,
        )
