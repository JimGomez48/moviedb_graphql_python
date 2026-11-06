from sqlalchemy.orm import Session

from moviedb.core.domain.actors import Actor, NewActor
from moviedb.core.pagination import PageParams
from moviedb.core.repositories.actors import ActorRepository


def test_create_returns_domain_model_with_generated_id(session: Session) -> None:
    # Arrange
    repo = ActorRepository(session)

    # Act
    created = repo.create(NewActor(first_name="Ada", last_name="Lovelace"))

    # Assert
    assert isinstance(created, Actor)
    assert created.id is not None
    assert (created.first_name, created.last_name) == ("Ada", "Lovelace")


def test_get_returns_domain_model_when_found(session: Session) -> None:
    # Arrange
    repo = ActorRepository(session)
    created = repo.create(NewActor(first_name="Ada", last_name="Lovelace"))

    # Act
    found = repo.get(created.id)

    # Assert
    assert found == created


def test_get_returns_none_when_missing(session: Session) -> None:
    # Arrange
    repo = ActorRepository(session)

    # Act
    found = repo.get(999)

    # Assert
    assert found is None


def test_list_page_returns_ordered_domain_models(session: Session) -> None:
    # Arrange
    repo = ActorRepository(session)
    for name in ("A", "B", "C"):
        repo.create(NewActor(first_name=name, last_name="X"))

    # Act
    page = repo.list_page(PageParams(page=1, size=2))

    # Assert
    assert page.total == 3
    assert page.params == PageParams(page=1, size=2)
    assert [a.first_name for a in page.items] == ["A", "B"]
    assert all(isinstance(a, Actor) for a in page.items)
