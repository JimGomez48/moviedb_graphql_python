from unittest.mock import create_autospec

import pytest

from moviedb.core.errors import NotFoundError
from moviedb.core.repositories.movies import MovieRepository
from moviedb.core.services.movies import MovieService
from moviedb.schemas.movies import MovieCreate, MovieRead


def test_get_raises_not_found_when_missing() -> None:
    # Arrange
    repo = create_autospec(MovieRepository, instance=True)
    repo.get.return_value = None

    # Act / Assert
    with pytest.raises(NotFoundError) as exc_info:
        MovieService(repo).get(3)
    assert str(exc_info.value) == "movie with id 3 was not found"


def test_create_delegates_to_repository() -> None:
    # Arrange
    repo = create_autospec(MovieRepository, instance=True)
    data = MovieCreate(title="Barbie", release_year=2023)
    repo.create.return_value = MovieRead(id=1, **data.model_dump())

    # Act
    created = MovieService(repo).create(data)

    # Assert
    assert created.id == 1
    repo.create.assert_called_once_with(data)
