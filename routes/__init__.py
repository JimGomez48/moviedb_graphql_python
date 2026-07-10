from fastapi import APIRouter, FastAPI

from routes import (
    actors,
    companies,
    directors,
    genres,
    movies,
    mpaa_ratings,
    reviews,
    system,
)
from routes.graphql import router as graphql_router

api_router = APIRouter()
api_router.include_router(system.router)
api_router.include_router(movies.router)
api_router.include_router(actors.router)
api_router.include_router(directors.router)
api_router.include_router(mpaa_ratings.router)
api_router.include_router(genres.router)
api_router.include_router(companies.router)
api_router.include_router(reviews.router)


def register_routes(app: FastAPI) -> None:
    app.include_router(api_router)
    app.include_router(graphql_router, prefix="/graphql")