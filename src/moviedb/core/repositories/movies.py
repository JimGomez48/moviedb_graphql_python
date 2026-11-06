from sqlalchemy.orm import Session

from moviedb.core.db.models import Movie
from moviedb.schemas.movies import MovieCreate, MovieRead

from .base import Repository


class MovieRepository(Repository[Movie, MovieRead, MovieCreate]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Movie, MovieRead)
