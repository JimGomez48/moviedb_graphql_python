from strawberry_sqlalchemy_mapper import StrawberrySQLAlchemyLoader

from moviedb.core.db.conn import get_session


async def get_graphql_context():
    session = get_session()

    try:
        yield {"sqlalchemy_loader": StrawberrySQLAlchemyLoader(bind=session)}
    finally:
        session.close()
