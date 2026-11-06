from fastapi.testclient import TestClient


def test_create_actor_returns_201_and_body(client: TestClient) -> None:
    # Act
    response = client.post(
        "/rest/actors/", json={"first_name": "Ada", "last_name": "L"}
    )

    # Assert
    assert response.status_code == 201
    assert response.json() == {"id": 1, "first_name": "Ada", "last_name": "L"}


def test_create_actor_rejects_invalid_body(client: TestClient) -> None:
    # Act
    response = client.post("/rest/actors/", json={"first_name": "Ada"})

    # Assert
    assert response.status_code == 422


def test_get_actor_returns_actor(client: TestClient) -> None:
    # Arrange
    created = client.post("/rest/actors/", json={"first_name": "Ada", "last_name": "L"})

    # Act
    response = client.get(f"/rest/actors/{created.json()['id']}")

    # Assert
    assert response.status_code == 200
    assert response.json() == created.json()


def test_get_actor_returns_404_when_missing(client: TestClient) -> None:
    # Act
    response = client.get("/rest/actors/999")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "actor with id 999 was not found"}


def test_list_actors_is_paginated(client: TestClient) -> None:
    # Arrange
    for name in ("A", "B", "C"):
        client.post("/rest/actors/", json={"first_name": name, "last_name": "X"})

    # Act
    response = client.get("/rest/actors/", params={"page": 2, "size": 2})

    # Assert
    body = response.json()
    assert response.status_code == 200
    assert body["total"] == 3
    assert [a["first_name"] for a in body["items"]] == ["C"]
