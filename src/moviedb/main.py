from contextlib import asynccontextmanager

from fastapi import FastAPI

from moviedb.core.db.conn import init_db
from moviedb.routes import register_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)
register_routes(app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("moviedb.main:app", host="0.0.0.0", port=8000)
