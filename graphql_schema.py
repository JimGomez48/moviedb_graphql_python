import strawberry
from sqlalchemy import select
from strawberry_sqlalchemy_mapper import StrawberrySQLAlchemyLoader, StrawberrySQLAlchemyMapper
from strawberry_sqlalchemy_mapper import field as sqlalchemy_field
from strawberry_sqlalchemy_mapper.field import connection_session

from db.conn import SessionLocal, get_session
from db.models import Movie

mapper = StrawberrySQLAlchemyMapper()


@mapper.type(Movie)
class MovieType:
    pass


@strawberry.type
class Query:
    @sqlalchemy_field(sessionmaker=get_session)
    def movies(self) -> list[MovieType]:
        session = connection_session.get()
        return list(session.scalars(select(Movie)).all())


mapper.finalize()

schema = strawberry.Schema(query=Query)


async def get_graphql_context():
    session = SessionLocal()
    try:
        yield {"sqlalchemy_loader": StrawberrySQLAlchemyLoader(bind=session)}
    finally:
        session.close()
