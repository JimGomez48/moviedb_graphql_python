from contextlib import asynccontextmanager

from fastapi import FastAPI

from db.conn import init_db
from routes import register_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)
register_routes(app)