from fastapi import FastAPI

from .rest import router as rest_router
from .gql import router as graphql_router


def register_routes(app: FastAPI) -> None:
    app.include_router(rest_router, prefix="/rest")
    app.include_router(graphql_router, prefix="/graphql")
