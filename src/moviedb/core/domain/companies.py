from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NewCompany:
    """Data needed to create a company; the database assigns the id."""

    name: str


@dataclass(frozen=True, slots=True)
class Company:
    id: int
    name: str
