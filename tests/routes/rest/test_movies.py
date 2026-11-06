from fastapi.testclient import TestClient


def test_create_movie_returns_201_and_body(client: TestClient) -> None:
    # Act
    response = client.post(
        "/rest/movies/", json={"title": "Barbie", "release_year": 2023}
    )

    # Assert
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "title": "Barbie",
        "release_year": 2023,
        "mpaa_rating_id": None,
    }


def test_create_movie_rejects_missing_title(client: TestClient) -> None:
    assert client.post("/rest/movies/", json={}).status_code == 422


def test_get_movie_returns_404_when_missing(client: TestClient) -> None:
    # Act
    response = client.get("/rest/movies/999")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "movie with id 999 was not found"}


def test_list_movies_is_paginated(client: TestClient) -> None:
    # Arrange
    for title in ("A", "B", "C"):
        client.post("/rest/movies/", json={"title": title})

    # Act
    response = client.get("/rest/movies/", params={"page": 1, "size": 2})

    # Assert
    assert response.json()["total"] == 3
    assert [m["title"] for m in response.json()["items"]] == ["A", "B"]
