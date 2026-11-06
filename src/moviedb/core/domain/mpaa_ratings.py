from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NewMpaaRating:
    """Data needed to create a mpaarating; the database assigns the id."""

    code: str
    description: str | None


@dataclass(frozen=True, slots=True)
class MpaaRating:
    id: int
    code: str
    description: str | None
