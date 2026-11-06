from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NewReview:
    """Data needed to create a review; the database assigns the id."""

    movie_id: int
    reviewer: str | None
    rating: int | None
    body: str | None


@dataclass(frozen=True, slots=True)
class Review:
    id: int
    movie_id: int
    reviewer: str | None
    rating: int | None
    body: str | None
