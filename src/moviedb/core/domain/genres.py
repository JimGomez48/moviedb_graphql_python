from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NewGenre:
    """Data needed to create a genre; the database assigns the id."""

    name: str


@dataclass(frozen=True, slots=True)
class Genre:
    id: int
    name: str
