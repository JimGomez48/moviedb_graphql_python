from sqlalchemy.orm import Session

from moviedb.core.db.models import Genre
from moviedb.schemas.genres import GenreCreate, GenreRead

from .base import Repository


class GenreRepository(Repository[Genre, GenreRead, GenreCreate]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Genre, GenreRead)
