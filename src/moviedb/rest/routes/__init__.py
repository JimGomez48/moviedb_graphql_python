from fastapi import APIRouter

from . import actors, companies, directors, genres, movies, mpaa_ratings, reviews

router = APIRouter()

router.include_router(movies.router)
router.include_router(actors.router)
router.include_router(directors.router)
router.include_router(mpaa_ratings.router)
router.include_router(genres.router)
router.include_router(companies.router)
router.include_router(reviews.router)
