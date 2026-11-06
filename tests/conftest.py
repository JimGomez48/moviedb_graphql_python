from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from moviedb.core.db.models import Base
from moviedb.dependencies import get_db_session
from moviedb.main import app


@pytest.fixture
def session() -> Iterator[Session]:
    """A session bound to a fresh in-memory SQLite database, one per test."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    with factory() as db_session:
        yield db_session
    engine.dispose()


@pytest.fixture
def client(session: Session) -> Iterator[TestClient]:
    app.dependency_overrides[get_db_session] = lambda: session
    # Deliberately not used as a context manager: that would run the lifespan
    # and touch the real SQLite file.
    yield TestClient(app)
    app.dependency_overrides.clear()
