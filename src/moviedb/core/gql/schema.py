import strawberry
from strawberry_sqlalchemy_mapper import (
    StrawberrySQLAlchemyMapper,
    field as sqlalchemy_field,
)
from strawberry_sqlalchemy_mapper.field import connection_session
from sqlalchemy import select

from moviedb.core.db.models import (
    Actor,
    Company,
    Director,
    Genre,
    Movie,
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


mapper.finalize()


@strawberry.type
class Query:
    @sqlalchemy_field
    def actors(self) -> list[ActorType]:
        return list(connection_session.get().scalars(select(Actor)).all())

    @sqlalchemy_field
    def directors(self) -> list[DirectorType]:
        return list(connection_session.get().scalars(select(Director)).all())

    @sqlalchemy_field
    def mpaa_ratings(self) -> list[MpaaRatingType]:
        return list(connection_session.get().scalars(select(MpaaRating)).all())

    @sqlalchemy_field
    def genres(self) -> list[GenreType]:
        return list(connection_session.get().scalars(select(Genre)).all())

    @sqlalchemy_field
    def companies(self) -> list[CompanyType]:
        return list(connection_session.get().scalars(select(Company)).all())

    @sqlalchemy_field
    def movies(self) -> list[MovieType]:
        return list(connection_session.get().scalars(select(Movie)).all())

    @sqlalchemy_field
    def reviews(self) -> list[ReviewType]:
        return list(connection_session.get().scalars(select(Review)).all())


schema = strawberry.Schema(query=Query)
