from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, Session

ModelType = TypeVar("ModelType", bound=DeclarativeBase)


def _get_or_create(
    session: Session, model: type[ModelType], **attributes: object
) -> ModelType:
    row = session.scalar(select(model).filter_by(**attributes))
    if row is None:
        row = model(**attributes)
        session.add(row)
        session.flush()
    return row


def seed_database(session_factory: type[Session]) -> None:
    """Seed the database with a small, connected movie catalog."""
    from db.models import (
        Actor,
        Company,
        Director,
        Genre,
        Movie,
        MovieActor,
        MovieActorRole,
        MovieCompany,
        MovieDirector,
        MovieGenre,
        MpaaRating,
        Review,
    )

    with session_factory() as session:
        rated_r = _get_or_create(
            session, MpaaRating, code="R", description="Restricted"
        )
        rated_pg13 = _get_or_create(
            session,
            MpaaRating,
            code="PG-13",
            description="Parents strongly cautioned",
        )

        science_fiction = _get_or_create(session, Genre, name="Science Fiction")
        action = _get_or_create(session, Genre, name="Action")
        thriller = _get_or_create(session, Genre, name="Thriller")

        warner_bros = _get_or_create(session, Company, name="Warner Bros.")
        legendary = _get_or_create(session, Company, name="Legendary Pictures")

        keanu_reeves = _get_or_create(
            session, Actor, first_name="Keanu", last_name="Reeves"
        )
        laurence_fishburne = _get_or_create(
            session, Actor, first_name="Laurence", last_name="Fishburne"
        )
        carrie_anne_moss = _get_or_create(
            session, Actor, first_name="Carrie-Anne", last_name="Moss"
        )
        leonardo_dicaprio = _get_or_create(
            session, Actor, first_name="Leonardo", last_name="DiCaprio"
        )
        joseph_gordon_levitt = _get_or_create(
            session, Actor, first_name="Joseph", last_name="Gordon-Levitt"
        )
        elliot_page = _get_or_create(
            session, Actor, first_name="Elliot", last_name="Page"
        )

        lana_wachowski = _get_or_create(
            session, Director, first_name="Lana", last_name="Wachowski"
        )
        lilly_wachowski = _get_or_create(
            session, Director, first_name="Lilly", last_name="Wachowski"
        )
        christopher_nolan = _get_or_create(
            session, Director, first_name="Christopher", last_name="Nolan"
        )

        matrix = _get_or_create(session, Movie, title="The Matrix", release_year=1999)
        inception = _get_or_create(session, Movie, title="Inception", release_year=2010)
        matrix.mpaa_rating = rated_r
        inception.mpaa_rating = rated_pg13
        session.flush()

        for movie, company in (
            (matrix, warner_bros),
            (inception, warner_bros),
            (inception, legendary),
        ):
            _get_or_create(
                session, MovieCompany, movie_id=movie.id, company_id=company.id
            )

        for movie, genre in (
            (matrix, science_fiction),
            (matrix, action),
            (inception, science_fiction),
            (inception, action),
            (inception, thriller),
        ):
            _get_or_create(session, MovieGenre, movie_id=movie.id, genre_id=genre.id)

        for movie, director in (
            (matrix, lana_wachowski),
            (matrix, lilly_wachowski),
            (inception, christopher_nolan),
        ):
            _get_or_create(
                session, MovieDirector, movie_id=movie.id, director_id=director.id
            )

        for movie, actor, role in (
            (matrix, keanu_reeves, "Neo"),
            (matrix, laurence_fishburne, "Morpheus"),
            (matrix, carrie_anne_moss, "Trinity"),
            (inception, leonardo_dicaprio, "Cobb"),
            (inception, joseph_gordon_levitt, "Arthur"),
            (inception, elliot_page, "Ariadne"),
        ):
            movie_actor = _get_or_create(
                session, MovieActor, movie_id=movie.id, actor_id=actor.id
            )
            _get_or_create(
                session,
                MovieActorRole,
                movie_actor_id=movie_actor.id,
                role=role,
            )

        _get_or_create(
            session,
            Review,
            movie_id=matrix.id,
            reviewer="Ada Lovelace",
            rating=5,
            body="A landmark science-fiction action film.",
        )
        _get_or_create(
            session,
            Review,
            movie_id=inception.id,
            reviewer="Alan Turing",
            rating=5,
            body="A smart, visually inventive heist thriller.",
        )
        session.commit()
