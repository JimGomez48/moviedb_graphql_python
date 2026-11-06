import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.entities import READ_ONLY_ENTITIES, EntitySpec
from tests.helpers import seed_entity

ids = [spec.name for spec in READ_ONLY_ENTITIES]


@pytest.mark.parametrize("spec", READ_ONLY_ENTITIES, ids=ids)
def test_get_returns_entity(
    client: TestClient, session: Session, spec: EntitySpec
) -> None:
    # Arrange
    seed_entity(session, spec)

    # Act
    response = client.get(f"/rest/{spec.path}/1")

    # Assert
    assert response.status_code == 200
    assert response.json() == spec.expected


@pytest.mark.parametrize("spec", READ_ONLY_ENTITIES, ids=ids)
def test_get_returns_404_when_missing(client: TestClient, spec: EntitySpec) -> None:
    # Act
    response = client.get(f"/rest/{spec.path}/999")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": f"{spec.name} with id 999 was not found"}


@pytest.mark.parametrize("spec", READ_ONLY_ENTITIES, ids=ids)
def test_list_is_paginated(
    client: TestClient, session: Session, spec: EntitySpec
) -> None:
    # Arrange
    seed_entity(session, spec, count=3)

    # Act
    response = client.get(f"/rest/{spec.path}/", params={"page": 1, "size": 2})

    # Assert
    body = response.json()
    assert response.status_code == 200
    assert body["total"] == 3
    assert len(body["items"]) == 2
    assert body["items"][0] == spec.expected


@pytest.mark.parametrize("spec", READ_ONLY_ENTITIES, ids=ids)
def test_entity_is_read_only(client: TestClient, spec: EntitySpec) -> None:
    # Act
    response = client.post(f"/rest/{spec.path}/", json=spec.seed)

    # Assert
    assert response.status_code == 405
