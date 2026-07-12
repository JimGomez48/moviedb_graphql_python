from pathlib import Path

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker

from db.models import Base
from db.seed import seed_database

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
    seed_database(SessionLocal)


def _migrate_existing_schema() -> None:
    """Apply the one additive change needed by the pre-existing SQLite database."""
    inspector = inspect(engine)
    if "movies" not in inspector.get_table_names():
        return

    movie_columns = {column["name"] for column in inspector.get_columns("movies")}
    if "mpaa_rating_id" not in movie_columns:
        with engine.begin() as connection:
            connection.execute(
                text("ALTER TABLE movies ADD COLUMN mpaa_rating_id INTEGER")
            )
