import strawberry
from sqlalchemy import select
from strawberry_sqlalchemy_mapper import (
    StrawberrySQLAlchemyLoader,
    StrawberrySQLAlchemyMapper,
)
from strawberry_sqlalchemy_mapper import field as sqlalchemy_field
from strawberry_sqlalchemy_mapper.field import connection_session

from moviedb.db.conn import SessionLocal, get_session
from moviedb.db.models import (
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

mapper = StrawberrySQLAlchemyMapper(
    model_to_type_name=lambda model: f"{model.__name__}Type"
)


@mapper.type(Movie)
class MovieType:
    pass


@mapper.type(Actor)
class ActorType:
    pass


@mapper.type(Director)
class DirectorType:
    pass


@mapper.type(MpaaRating)
class MpaaRatingType:
    pass


@mapper.type(Genre)
class GenreType:
    pass


@mapper.type(Company)
class CompanyType:
    pass


@mapper.type(Review)
class ReviewType:
    pass


@mapper.type(MovieCompany)
class MovieCompanyType:
    pass


@mapper.type(MovieActor)
class MovieActorType:
    pass


@mapper.type(MovieActorRole)
class MovieActorRoleType:
    pass


@mapper.type(MovieDirector)
class MovieDirectorType:
    pass


@mapper.type(MovieGenre)
class MovieGenreType:
    pass


@strawberry.type
class Query:
    @sqlalchemy_field(sessionmaker=get_session)
    def actors(self) -> list[ActorType]:
        return list(connection_session.get().scalars(select(Actor)).all())

    @sqlalchemy_field(sessionmaker=get_session)
    def directors(self) -> list[DirectorType]:
        return list(connection_session.get().scalars(select(Director)).all())

    @sqlalchemy_field(sessionmaker=get_session)
    def mpaa_ratings(self) -> list[MpaaRatingType]:
        return list(connection_session.get().scalars(select(MpaaRating)).all())

    @sqlalchemy_field(sessionmaker=get_session)
    def genres(self) -> list[GenreType]:
        return list(connection_session.get().scalars(select(Genre)).all())

    @sqlalchemy_field(sessionmaker=get_session)
    def companies(self) -> list[CompanyType]:
        return list(connection_session.get().scalars(select(Company)).all())

    @sqlalchemy_field(sessionmaker=get_session)
    def movies(self) -> list[MovieType]:
        return list(connection_session.get().scalars(select(Movie)).all())

    @sqlalchemy_field(sessionmaker=get_session)
    def reviews(self) -> list[ReviewType]:
        return list(connection_session.get().scalars(select(Review)).all())

    @sqlalchemy_field(sessionmaker=get_session)
    def movie_companies(self) -> list[MovieCompanyType]:
        return list(connection_session.get().scalars(select(MovieCompany)).all())

    @sqlalchemy_field(sessionmaker=get_session)
    def movie_actors(self) -> list[MovieActorType]:
        return list(connection_session.get().scalars(select(MovieActor)).all())

    @sqlalchemy_field(sessionmaker=get_session)
    def movie_actor_roles(self) -> list[MovieActorRoleType]:
        return list(connection_session.get().scalars(select(MovieActorRole)).all())

    @sqlalchemy_field(sessionmaker=get_session)
    def movie_directors(self) -> list[MovieDirectorType]:
        return list(connection_session.get().scalars(select(MovieDirector)).all())

    @sqlalchemy_field(sessionmaker=get_session)
    def movie_genres(self) -> list[MovieGenreType]:
        return list(connection_session.get().scalars(select(MovieGenre)).all())


mapper.finalize()

schema = strawberry.Schema(query=Query)


async def get_graphql_context():
    session = SessionLocal()
    try:
        yield {"sqlalchemy_loader": StrawberrySQLAlchemyLoader(bind=session)}
    finally:
        session.close()
