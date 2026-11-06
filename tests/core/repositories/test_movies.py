from sqlalchemy.orm import Session

from moviedb.core.repositories.movies import MovieRepository
from moviedb.schemas.movies import MovieCreate, MovieRead


def test_create_and_get_round_trip_as_schema(session: Session) -> None:
    # Arrange
    repo = MovieRepository(session)

    # Act
    created = repo.create(MovieCreate(title="Barbie", release_year=2023))
    found = repo.get(created.id)

    # Assert
    assert isinstance(created, MovieRead)
    assert found == created
    assert (created.title, created.release_year, created.mpaa_rating_id) == (
        "Barbie",
        2023,
        None,
    )
