from contextlib import asynccontextmanager

from fastapi import FastAPI

from moviedb.core.db.conn import init_db
from moviedb.gql import router as graphql_router
from moviedb.rest.errors import register_exception_handlers
from moviedb.rest.routes import router as rest_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

register_exception_handlers(app)

app.include_router(rest_router, prefix="/rest")
app.include_router(graphql_router, prefix="/graphql", tags=["graphql"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("moviedb.main:app", host="0.0.0.0", port=8000, reload=True)
