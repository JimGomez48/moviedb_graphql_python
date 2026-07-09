from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, sessionmaker
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
    _seed_movies()


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
