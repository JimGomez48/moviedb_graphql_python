from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from moviedb.dependencies import get_db_session
from moviedb.main import app


@pytest.fixture
def client(session: Session) -> Iterator[TestClient]:
    app.dependency_overrides[get_db_session] = lambda: session
    # Deliberately not used as a context manager: that would run the lifespan
    # and touch the real SQLite file.
    yield TestClient(app)
    app.dependency_overrides.clear()
