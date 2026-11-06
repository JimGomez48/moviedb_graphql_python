from sqlalchemy.orm import Session

from moviedb.core.domain.movies import Movie, NewMovie
from moviedb.core.repositories.movies import MovieRepository


def test_create_and_get_round_trip_as_domain_model(session: Session) -> None:
    # Arrange
    repo = MovieRepository(session)

    # Act
    created = repo.create(NewMovie(title="Barbie", release_year=2023))
    found = repo.get(created.id)

    # Assert
    assert isinstance(created, Movie)
    assert found == created
    assert (created.title, created.release_year, created.mpaa_rating_id) == (
        "Barbie",
        2023,
        None,
    )
