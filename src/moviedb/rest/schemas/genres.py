from pydantic import BaseModel

from moviedb.core.domain.genres import Genre, NewGenre


class GenreBase(BaseModel):
    name: str


class GenreCreate(GenreBase):
    def to_domain(self) -> NewGenre:
        return NewGenre(
            name=self.name,
        )


class GenreRead(GenreBase):
    id: int

    @classmethod
    def from_domain(cls, domain: Genre) -> GenreRead:
        return cls(
            id=domain.id,
            name=domain.name,
        )
