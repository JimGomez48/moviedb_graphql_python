"""A small connected catalog used by relationship and GraphQL tests.

Ids follow insertion order. Movies: 1 Matrix (R), 2 Speed (R), 3 Untitled (no rating).
"""

from sqlalchemy.orm import Session

from moviedb.core.db import models as m


def seed_catalog(session: Session) -> None:
    session.add_all(
        [
            m.MpaaRating(code="R", description="Restricted"),
            m.MpaaRating(code="PG", description="Parental Guidance"),
        ]
    )
    session.flush()
    session.add_all(
        [
            m.Movie(title="Matrix", release_year=1999, mpaa_rating_id=1),
            m.Movie(title="Speed", release_year=1994, mpaa_rating_id=1),
            m.Movie(title="Untitled"),
            m.Actor(first_name="Keanu", last_name="Reeves"),
            m.Actor(first_name="Laurence", last_name="Fishburne"),
            m.Director(first_name="Lana", last_name="Wachowski"),
            m.Genre(name="Science Fiction"),
            m.Genre(name="Action"),
            m.Company(name="Warner Bros."),
        ]
    )
    session.flush()
    neo = m.MovieActor(movie_id=1, actor_id=1)
    morpheus = m.MovieActor(movie_id=1, actor_id=2)
    session.add_all(
        [
            neo,
            morpheus,
            m.MovieActor(movie_id=2, actor_id=1, roles=[m.MovieActorRole(role="Jack")]),
            m.MovieDirector(movie_id=1, director_id=1),
            m.MovieGenre(movie_id=1, genre_id=1),
            m.MovieGenre(movie_id=1, genre_id=2),
            m.MovieGenre(movie_id=2, genre_id=2),
            m.MovieCompany(movie_id=1, company_id=1),
            m.MovieCompany(movie_id=2, company_id=1),
            m.Review(movie_id=1, reviewer="Sam", rating=5, body="Great"),
            m.Review(movie_id=1, reviewer="Alex", rating=4, body="Good"),
            m.Review(movie_id=2, reviewer="Sam", rating=3, body="Fast"),
        ]
    )
    session.flush()
    neo.roles = [m.MovieActorRole(role="Neo"), m.MovieActorRole(role="Thomas")]
    morpheus.roles = [m.MovieActorRole(role="Morpheus")]
    session.commit()


def add_movies(session: Session, count: int) -> None:
    """Add movies that each carry a rating, review, cast member, genre and company."""
    for index in range(count):
        movie = m.Movie(title=f"Extra {index}", mpaa_rating_id=1 + index % 2)
        session.add(movie)
        session.flush()
        session.add_all(
            [
                m.Review(movie_id=movie.id, body=f"Review {index}"),
                m.MovieActor(
                    movie_id=movie.id,
                    actor_id=1,
                    roles=[m.MovieActorRole(role="Cameo")],
                ),
                m.MovieDirector(movie_id=movie.id, director_id=1),
                m.MovieGenre(movie_id=movie.id, genre_id=1),
                m.MovieCompany(movie_id=movie.id, company_id=1),
            ]
        )
    session.commit()
