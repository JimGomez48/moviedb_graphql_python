from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NewMovie:
    """Data needed to create a movie; the database assigns the id."""

    title: str
    release_year: int | None = None
    mpaa_rating_id: int | None = None


@dataclass(frozen=True, slots=True)
class Movie:
    id: int
    title: str
    release_year: int | None
    mpaa_rating_id: int | None
