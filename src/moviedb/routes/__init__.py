from fastapi import FastAPI

from .errors import register_exception_handlers
from .gql import router as graphql_router
from .rest import router as rest_router


def register_routes(app: FastAPI) -> None:
    register_exception_handlers(app)
    app.include_router(rest_router, prefix="/rest")
    app.include_router(graphql_router, prefix="/graphql", tags=["graphql"])
