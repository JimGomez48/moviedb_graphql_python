from typing import Any

import pytest

from moviedb.core.domain import (
    actors,
    companies,
    directors,
    genres,
    movies,
    mpaa_ratings,
    reviews,
)
from moviedb.rest.schemas import (
    actors as rest_actors,
)
from moviedb.rest.schemas import (
    companies as rest_companies,
)
from moviedb.rest.schemas import (
    directors as rest_directors,
)
from moviedb.rest.schemas import (
    genres as rest_genres,
)
from moviedb.rest.schemas import (
    movies as rest_movies,
)
from moviedb.rest.schemas import (
    mpaa_ratings as rest_mpaa_ratings,
)
from moviedb.rest.schemas import (
    reviews as rest_reviews,
)

READ_CASES: list[tuple[type, Any, dict[str, Any]]] = [
    (
        rest_actors.ActorRead,
        actors.Actor(id=1, first_name="Ada", last_name="Lovelace"),
        {"id": 1, "first_name": "Ada", "last_name": "Lovelace"},
    ),
    (
        rest_directors.DirectorRead,
        directors.Director(id=2, first_name="Greta", last_name="Gerwig"),
        {"id": 2, "first_name": "Greta", "last_name": "Gerwig"},
    ),
    (
        rest_companies.CompanyRead,
        companies.Company(id=3, name="A24"),
        {"id": 3, "name": "A24"},
    ),
    (
        rest_genres.GenreRead,
        genres.Genre(id=4, name="Drama"),
        {"id": 4, "name": "Drama"},
    ),
    (
        rest_mpaa_ratings.MpaaRatingRead,
        mpaa_ratings.MpaaRating(id=5, code="PG", description=None),
        {"id": 5, "code": "PG", "description": None},
    ),
    (
        rest_movies.MovieRead,
        movies.Movie(id=6, title="Heat", release_year=None, mpaa_rating_id=5),
        {"id": 6, "title": "Heat", "release_year": None, "mpaa_rating_id": 5},
    ),
    (
        rest_reviews.ReviewRead,
        reviews.Review(id=7, movie_id=6, reviewer=None, rating=4, body="Good"),
        {"id": 7, "movie_id": 6, "reviewer": None, "rating": 4, "body": "Good"},
    ),
]


@pytest.mark.parametrize(
    ("read_cls", "domain", "expected"),
    READ_CASES,
    ids=[case[0].__name__ for case in READ_CASES],
)
def test_read_model_is_built_from_domain(
    read_cls: Any, domain: Any, expected: dict[str, Any]
) -> None:
    # Arrange / Act
    model = read_cls.from_domain(domain)

    # Assert
    assert isinstance(model, read_cls)
    assert model.model_dump() == expected


def test_actor_create_maps_to_new_domain_actor() -> None:
    # Arrange
    body = rest_actors.ActorCreate(first_name="Ada", last_name="Lovelace")

    # Act
    new = body.to_domain()

    # Assert
    assert new == actors.NewActor(first_name="Ada", last_name="Lovelace")


def test_movie_create_maps_optional_fields_to_new_domain_movie() -> None:
    # Arrange
    body = rest_movies.MovieCreate(title="Heat")

    # Act
    new = body.to_domain()

    # Assert
    assert new == movies.NewMovie(title="Heat", release_year=None, mpaa_rating_id=None)
