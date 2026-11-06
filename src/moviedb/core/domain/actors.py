from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NewActor:
    """Data needed to create a actor; the database assigns the id."""

    first_name: str
    last_name: str


@dataclass(frozen=True, slots=True)
class Actor:
    id: int
    first_name: str
    last_name: str


@dataclass(frozen=True, slots=True)
class CastMember:
    """An actor's participation in one movie, with the roles they played."""

    actor: Actor
    roles: tuple[str, ...]
