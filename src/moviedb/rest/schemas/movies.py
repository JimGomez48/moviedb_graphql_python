from pydantic import BaseModel

from moviedb.core.domain.movies import Movie, NewMovie


class MovieBase(BaseModel):
    title: str
    release_year: int | None = None
    mpaa_rating_id: int | None = None


class MovieCreate(MovieBase):
    def to_domain(self) -> NewMovie:
        return NewMovie(
            title=self.title,
            release_year=self.release_year,
            mpaa_rating_id=self.mpaa_rating_id,
        )


class MovieRead(MovieBase):
    id: int

    @classmethod
    def from_domain(cls, domain: Movie) -> MovieRead:
        return cls(
            id=domain.id,
            title=domain.title,
            release_year=domain.release_year,
            mpaa_rating_id=domain.mpaa_rating_id,
        )
