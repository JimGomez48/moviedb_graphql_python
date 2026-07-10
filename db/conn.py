from pathlib import Path

from sqlalchemy import create_engine, inspect, select, text
from sqlalchemy.orm import sessionmaker

from db.models import Base

DATABASE_PATH = Path(__file__).resolve().parent / "moviedb.sqlite"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_session():
    return SessionLocal()


def init_db() -> None:
    import db.models as models  # noqa: F401

    Base.metadata.create_all(bind=engine)
    _migrate_existing_schema()
    _seed_movies()


def _migrate_existing_schema() -> None:
    """Apply the one additive change needed by the pre-existing SQLite database."""
    inspector = inspect(engine)
    if "movies" not in inspector.get_table_names():
        return

    movie_columns = {column["name"] for column in inspector.get_columns("movies")}
    if "mpaa_rating_id" not in movie_columns:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE movies ADD COLUMN mpaa_rating_id INTEGER"))


def _seed_movies() -> None:
    from db.models import Movie

    with SessionLocal() as session:
        if session.scalar(select(Movie.id).limit(1)) is not None:
            return

        session.add_all(
            [
                Movie(title="The Matrix", release_year=1999),
                Movie(title="Inception", release_year=2010),
            ]
        )
        session.commit()