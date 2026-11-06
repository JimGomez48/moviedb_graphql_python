from typing import Any

from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.orm import Session

from tests.catalog import add_movies, seed_catalog


def run(client: TestClient, query: str) -> dict[str, Any]:
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    return response.json()


def test_list_query_returns_paged_entities(
    client: TestClient, session: Session
) -> None:
    # Arrange
    seed_catalog(session)

    # Act
    page_one = run(client, "{ movies(page: 1, size: 2) { id title releaseYear } }")
    page_two = run(client, "{ movies(page: 2, size: 2) { title } }")

    # Assert
    assert page_one["data"]["movies"] == [
        {"id": 1, "title": "Matrix", "releaseYear": 1999},
        {"id": 2, "title": "Speed", "releaseYear": 1994},
    ]
    assert page_two["data"]["movies"] == [{"title": "Untitled"}]


def test_every_entity_has_a_list_query(client: TestClient, session: Session) -> None:
    # Arrange
    seed_catalog(session)

    # Act
    body = run(
        client,
        """{ actors { firstName } directors { lastName } mpaaRatings { code }
             genres { name } companies { name } reviews { body } }""",
    )

    # Assert
    assert "errors" not in body
    assert {key: len(value) for key, value in body["data"].items()} == {
        "actors": 2,
        "directors": 1,
        "mpaaRatings": 2,
        "genres": 2,
        "companies": 1,
        "reviews": 3,
    }


def test_list_query_rejects_oversized_page(client: TestClient) -> None:
    # Arrange / Act
    body = run(client, "{ movies(size: 1000) { id } }")

    # Assert
    assert body["errors"]
    assert body["data"] is None


def test_get_by_id_returns_entity_or_null(client: TestClient, session: Session) -> None:
    # Arrange
    seed_catalog(session)

    # Act
    found = run(client, "{ actor(id: 1) { firstName lastName } }")
    missing = run(client, "{ actor(id: 999) { firstName } }")

    # Assert
    assert found["data"]["actor"] == {"firstName": "Keanu", "lastName": "Reeves"}
    assert missing == {"data": {"actor": None}}


def test_movie_exposes_related_entities(client: TestClient, session: Session) -> None:
    # Arrange
    seed_catalog(session)

    # Act
    body = run(
        client,
        """{ movie(id: 1) {
              title
              mpaaRating { code }
              reviews { reviewer body }
              cast { actor { firstName } roles }
              directors { lastName }
              genres { name }
              companies { name }
        } }""",
    )

    # Assert
    assert body["data"]["movie"] == {
        "title": "Matrix",
        "mpaaRating": {"code": "R"},
        "reviews": [
            {"reviewer": "Sam", "body": "Great"},
            {"reviewer": "Alex", "body": "Good"},
        ],
        "cast": [
            {"actor": {"firstName": "Keanu"}, "roles": ["Neo", "Thomas"]},
            {"actor": {"firstName": "Laurence"}, "roles": ["Morpheus"]},
        ],
        "directors": [{"lastName": "Wachowski"}],
        "genres": [{"name": "Science Fiction"}, {"name": "Action"}],
        "companies": [{"name": "Warner Bros."}],
    }


def test_movie_without_relations_returns_null_and_empty_lists(
    client: TestClient, session: Session
) -> None:
    # Arrange
    seed_catalog(session)

    # Act
    body = run(
        client, "{ movie(id: 3) { mpaaRating { code } reviews { id } cast { roles } } }"
    )

    # Assert
    assert body["data"]["movie"] == {"mpaaRating": None, "reviews": [], "cast": []}


def test_reverse_relations_resolve_to_movies(
    client: TestClient, session: Session
) -> None:
    # Arrange
    seed_catalog(session)

    # Act
    body = run(
        client,
        """{
          actor(id: 1) { movies { title } }
          director(id: 1) { movies { title } }
          genre(id: 2) { movies { title } }
          company(id: 1) { movies { title } }
          mpaaRating(id: 1) { movies { title } }
          review(id: 3) { movie { title } }
        }""",
    )

    # Assert
    titles = lambda movies: [movie["title"] for movie in movies]
    data = body["data"]
    assert titles(data["actor"]["movies"]) == ["Matrix", "Speed"]
    assert titles(data["director"]["movies"]) == ["Matrix"]
    assert titles(data["genre"]["movies"]) == ["Matrix", "Speed"]
    assert titles(data["company"]["movies"]) == ["Matrix", "Speed"]
    assert titles(data["mpaaRating"]["movies"]) == ["Matrix", "Speed"]
    assert data["review"]["movie"] == {"title": "Speed"}


def test_nested_query_does_not_issue_n_plus_one_queries(
    client: TestClient, session: Session
) -> None:
    # Arrange
    seed_catalog(session)
    query = """{ movies(size: 100) {
        mpaaRating { code } reviews { body } cast { actor { firstName } roles }
        directors { id } genres { name } companies { name }
    } }"""
    statements: list[str] = []
    engine = session.get_bind()
    event.listen(
        engine, "before_cursor_execute", lambda *args: statements.append(args[2])
    )
    run(client, query)
    baseline = len(statements)

    add_movies(session, 10)
    statements.clear()

    # Act
    body = run(client, query)

    # Assert
    assert "errors" not in body
    assert len(body["data"]["movies"]) == 13
    assert len(statements) == baseline
