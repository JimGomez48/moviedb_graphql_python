from sqlalchemy.orm import Session

from moviedb.core.domain.actors import Actor, CastMember
from moviedb.core.repositories.actors import ActorRepository
from moviedb.core.repositories.companies import CompanyRepository
from moviedb.core.repositories.directors import DirectorRepository
from moviedb.core.repositories.genres import GenreRepository
from moviedb.core.repositories.movies import MovieRepository
from moviedb.core.repositories.mpaa_ratings import MpaaRatingRepository
from moviedb.core.repositories.reviews import ReviewRepository
from tests.catalog import seed_catalog


def _titles(by_owner: dict[int, list]) -> dict[int, list[str]]:
    return {key: [movie.title for movie in movies] for key, movies in by_owner.items()}


def test_get_many_returns_only_existing_entities_keyed_by_id(session: Session) -> None:
    # Arrange
    seed_catalog(session)

    # Act
    found = MpaaRatingRepository(session).get_many([1, 2, 999])

    # Assert
    assert {key: rating.code for key, rating in found.items()} == {1: "R", 2: "PG"}


def test_get_many_with_no_ids_returns_empty(session: Session) -> None:
    # Arrange / Act
    found = MovieRepository(session).get_many([])

    # Assert
    assert found == {}


def test_movies_grouped_by_mpaa_rating(session: Session) -> None:
    # Arrange
    seed_catalog(session)

    # Act
    grouped = MovieRepository(session).list_by_mpaa_rating_ids([1, 2])

    # Assert
    assert _titles(grouped) == {1: ["Matrix", "Speed"]}


def test_reviews_grouped_by_movie(session: Session) -> None:
    # Arrange
    seed_catalog(session)

    # Act
    grouped = ReviewRepository(session).list_by_movie_ids([1, 2, 3])

    # Assert
    assert {key: [r.body for r in reviews] for key, reviews in grouped.items()} == {
        1: ["Great", "Good"],
        2: ["Fast"],
    }


def test_genres_directors_companies_grouped_by_movie(session: Session) -> None:
    # Arrange
    seed_catalog(session)

    # Act
    genres = GenreRepository(session).list_by_movie_ids([1, 2])
    directors = DirectorRepository(session).list_by_movie_ids([1, 2])
    companies = CompanyRepository(session).list_by_movie_ids([1, 2])

    # Assert
    assert {k: [g.name for g in v] for k, v in genres.items()} == {
        1: ["Science Fiction", "Action"],
        2: ["Action"],
    }
    assert {k: [d.last_name for d in v] for k, v in directors.items()} == {
        1: ["Wachowski"]
    }
    assert {k: [c.name for c in v] for k, v in companies.items()} == {
        1: ["Warner Bros."],
        2: ["Warner Bros."],
    }


def test_cast_grouped_by_movie_includes_roles(session: Session) -> None:
    # Arrange
    seed_catalog(session)

    # Act
    cast = ActorRepository(session).cast_by_movie_ids([1, 2, 3])

    # Assert
    assert set(cast) == {1, 2}
    assert all(isinstance(member, CastMember) for member in cast[1])
    assert [(c.actor.first_name, c.roles) for c in cast[1]] == [
        ("Keanu", ("Neo", "Thomas")),
        ("Laurence", ("Morpheus",)),
    ]
    assert isinstance(cast[2][0].actor, Actor)
    assert cast[2][0].roles == ("Jack",)


def test_movies_grouped_by_actor_director_genre_company(session: Session) -> None:
    # Arrange
    seed_catalog(session)
    repo = MovieRepository(session)

    # Act / Assert
    assert _titles(repo.list_by_actor_ids([1, 2])) == {
        1: ["Matrix", "Speed"],
        2: ["Matrix"],
    }
    assert _titles(repo.list_by_director_ids([1])) == {1: ["Matrix"]}
    assert _titles(repo.list_by_genre_ids([1, 2])) == {
        1: ["Matrix"],
        2: ["Matrix", "Speed"],
    }
    assert _titles(repo.list_by_company_ids([1])) == {1: ["Matrix", "Speed"]}
