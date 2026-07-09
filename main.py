from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import select
from strawberry.fastapi import GraphQLRouter

from db.conn import SessionLocal, init_db
from db.models import Movie
from graphql_schema import get_graphql_context, schema


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def hello():
    return {"message": "Hello, World!"}


@app.get("/movies")
def list_movies():
    with SessionLocal() as session:
        movies = session.scalars(select(Movie)).all()
        return [
            {"id": movie.id, "title": movie.title, "release_year": movie.release_year}
            for movie in movies
        ]


graphql_app = GraphQLRouter(schema, context_getter=get_graphql_context)
app.include_router(graphql_app, prefix="/graphql")
