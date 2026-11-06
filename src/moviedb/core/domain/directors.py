from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NewDirector:
    """Data needed to create a director; the database assigns the id."""

    first_name: str
    last_name: str


@dataclass(frozen=True, slots=True)
class Director:
    id: int
    first_name: str
    last_name: str
