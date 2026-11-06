from unittest.mock import create_autospec

import pytest

from moviedb.core.repositories.actors import ActorRepository
from moviedb.core.repositories.companies import CompanyRepository
from moviedb.core.repositories.directors import DirectorRepository
from moviedb.core.repositories.genres import GenreRepository
from moviedb.core.repositories.movies import MovieRepository
from moviedb.core.repositories.mpaa_ratings import MpaaRatingRepository
from moviedb.core.repositories.reviews import ReviewRepository
from moviedb.core.services.actors import ActorService
from moviedb.core.services.companies import CompanyService
from moviedb.core.services.directors import DirectorService
from moviedb.core.services.genres import GenreService
from moviedb.core.services.movies import MovieService
from moviedb.core.services.mpaa_ratings import MpaaRatingService
from moviedb.core.services.reviews import ReviewService

# (repository class, service class, method name) - services delegate by the same name.
DELEGATIONS = [
    (MpaaRatingRepository, MpaaRatingService, "get_many"),
    (MovieRepository, MovieService, "get_many"),
    (MovieRepository, MovieService, "list_by_mpaa_rating_ids"),
    (MovieRepository, MovieService, "list_by_actor_ids"),
    (MovieRepository, MovieService, "list_by_director_ids"),
    (MovieRepository, MovieService, "list_by_genre_ids"),
    (MovieRepository, MovieService, "list_by_company_ids"),
    (ReviewRepository, ReviewService, "list_by_movie_ids"),
    (ActorRepository, ActorService, "cast_by_movie_ids"),
    (DirectorRepository, DirectorService, "list_by_movie_ids"),
    (GenreRepository, GenreService, "list_by_movie_ids"),
    (CompanyRepository, CompanyService, "list_by_movie_ids"),
]


@pytest.mark.parametrize(
    ("repo_cls", "service_cls", "method"),
    DELEGATIONS,
    ids=[f"{s.__name__}.{m}" for _, s, m in DELEGATIONS],
)
def test_service_delegates_batch_lookup_to_repository(
    repo_cls: type, service_cls: type, method: str
) -> None:
    # Arrange
    repo = create_autospec(repo_cls, instance=True)
    sentinel = {1: []}
    getattr(repo, method).return_value = sentinel
    service = service_cls(repo)

    # Act
    result = getattr(service, method)([1, 2])

    # Assert
    assert result is sentinel
    getattr(repo, method).assert_called_once_with([1, 2])
