from fastapi import APIRouter, Depends
from fastapi_pagination import Page, pagination_ctx

from moviedb.core.db.conn import SessionLocal
from moviedb.core.db.models import Movie
from moviedb.schemas.movies import MovieCreate, MovieRead

from .utils import get_row_or_404, paginate_rows

router = APIRouter(prefix="/movies", tags=["movies"])

ListPage = Page[MovieRead]
list_pagination = Depends(pagination_ctx(ListPage))


@router.get("/", dependencies=[list_pagination])
def list_movies() -> ListPage:
    with SessionLocal() as session:
        return paginate_rows(session, Movie, MovieRead)


@router.get("/{entity_id}")
def get_movie(entity_id: int) -> MovieRead:
    with SessionLocal() as session:
        return MovieRead.model_validate(
            get_row_or_404(session, Movie, "movie", entity_id)
        )


@router.post("/", status_code=201)
def create_movie(movie: MovieCreate) -> MovieRead:
    with SessionLocal() as session:
        db_movie = Movie(**movie.model_dump())
        session.add(db_movie)
        session.commit()
        session.refresh(db_movie)
        return MovieRead.model_validate(db_movie)
