"""Per-request dataloaders that batch relationship lookups through services."""

from collections.abc import Callable, Collection

from strawberry.dataloader import DataLoader

from moviedb.core.domain.actors import CastMember
from moviedb.core.domain.companies import Company
from moviedb.core.domain.directors import Director
from moviedb.core.domain.genres import Genre
from moviedb.core.domain.movies import Movie
from moviedb.core.domain.mpaa_ratings import MpaaRating
from moviedb.core.domain.reviews import Review
from moviedb.core.services.actors import ActorService
from moviedb.core.services.companies import CompanyService
from moviedb.core.services.directors import DirectorService
from moviedb.core.services.genres import GenreService
from moviedb.core.services.movies import MovieService
from moviedb.core.services.mpaa_ratings import MpaaRatingService
from moviedb.core.services.reviews import ReviewService


def _one_per_key[T](
    fetch: Callable[[Collection[int]], dict[int, T]],
) -> DataLoader[int, T | None]:
    async def load(keys: list[int]) -> list[T | None]:
        found = fetch(keys)
        return [found.get(key) for key in keys]

    return DataLoader(load_fn=load)


def _many_per_key[T](
    fetch: Callable[[Collection[int]], dict[int, list[T]]],
) -> DataLoader[int, list[T]]:
    async def load(keys: list[int]) -> list[list[T]]:
        found = fetch(keys)
        return [found.get(key, []) for key in keys]

    return DataLoader(load_fn=load)


class Loaders:
    """One dataloader per relationship; build a new instance for every request."""

    def __init__(
        self,
        *,
        actors: ActorService,
        companies: CompanyService,
        directors: DirectorService,
        genres: GenreService,
        movies: MovieService,
        mpaa_ratings: MpaaRatingService,
        reviews: ReviewService,
    ) -> None:
        # Many-to-one: movie -> rating, review -> movie.
        self.mpaa_rating: DataLoader[int, MpaaRating | None] = _one_per_key(
            mpaa_ratings.get_many
        )
        self.movie: DataLoader[int, Movie | None] = _one_per_key(movies.get_many)

        # One-to-many and many-to-many, grouped by the owning entity's id.
        self.reviews_by_movie: DataLoader[int, list[Review]] = _many_per_key(
            reviews.list_by_movie_ids
        )
        self.cast_by_movie: DataLoader[int, list[CastMember]] = _many_per_key(
            actors.cast_by_movie_ids
        )
        self.directors_by_movie: DataLoader[int, list[Director]] = _many_per_key(
            directors.list_by_movie_ids
        )
        self.genres_by_movie: DataLoader[int, list[Genre]] = _many_per_key(
            genres.list_by_movie_ids
        )
        self.companies_by_movie: DataLoader[int, list[Company]] = _many_per_key(
            companies.list_by_movie_ids
        )
        self.movies_by_mpaa_rating: DataLoader[int, list[Movie]] = _many_per_key(
            movies.list_by_mpaa_rating_ids
        )
        self.movies_by_actor: DataLoader[int, list[Movie]] = _many_per_key(
            movies.list_by_actor_ids
        )
        self.movies_by_director: DataLoader[int, list[Movie]] = _many_per_key(
            movies.list_by_director_ids
        )
        self.movies_by_genre: DataLoader[int, list[Movie]] = _many_per_key(
            movies.list_by_genre_ids
        )
        self.movies_by_company: DataLoader[int, list[Movie]] = _many_per_key(
            movies.list_by_company_ids
        )
