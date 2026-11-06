from sqlalchemy.orm import Session

from moviedb.core.db.models import Director
from moviedb.schemas.directors import DirectorCreate, DirectorRead

from .base import Repository


class DirectorRepository(Repository[Director, DirectorRead, DirectorCreate]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Director, DirectorRead)
