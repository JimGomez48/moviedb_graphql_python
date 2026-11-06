import dataclasses
from unittest.mock import create_autospec

import pytest

from moviedb.core.domain.actors import Actor, NewActor
from moviedb.core.errors import NotFoundError
from moviedb.core.pagination import PageParams, PageResult
from moviedb.core.repositories.actors import ActorRepository
from moviedb.core.services.actors import ActorService


def test_get_returns_actor_from_repository() -> None:
    # Arrange
    repo = create_autospec(ActorRepository, instance=True)
    repo.get.return_value = Actor(id=1, first_name="Ada", last_name="Lovelace")
    service = ActorService(repo)

    # Act
    actor = service.get(1)

    # Assert
    assert actor.id == 1
    repo.get.assert_called_once_with(1)


def test_get_raises_not_found_when_missing() -> None:
    # Arrange
    repo = create_autospec(ActorRepository, instance=True)
    repo.get.return_value = None
    service = ActorService(repo)

    # Act / Assert
    with pytest.raises(NotFoundError) as exc_info:
        service.get(42)
    assert str(exc_info.value) == "actor with id 42 was not found"


def test_create_delegates_to_repository() -> None:
    # Arrange
    repo = create_autospec(ActorRepository, instance=True)
    data = NewActor(first_name="Ada", last_name="Lovelace")
    repo.create.return_value = Actor(id=7, **dataclasses.asdict(data))
    service = ActorService(repo)

    # Act
    created = service.create(data)

    # Assert
    assert created.id == 7
    repo.create.assert_called_once_with(data)


def test_list_delegates_paging_to_repository() -> None:
    # Arrange
    repo = create_autospec(ActorRepository, instance=True)
    params = PageParams(page=2, size=5)
    expected = PageResult(items=[], total=0, params=params)
    repo.list_page.return_value = expected
    service = ActorService(repo)

    # Act
    result = service.list(params)

    # Assert
    assert result is expected
    repo.list_page.assert_called_once_with(params)
