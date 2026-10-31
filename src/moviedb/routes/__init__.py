from fastapi import FastAPI

from .gql import router as graphql_router
from .rest import router as rest_router


def register_routes(app: FastAPI) -> None:
    app.include_router(rest_router, prefix="/rest")
    app.include_router(graphql_router, prefix="/graphql", tags=["graphql"])
