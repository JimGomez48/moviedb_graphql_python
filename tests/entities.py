"""Spec table for the read-only entities (actors are covered in dedicated tests)."""

from dataclasses import dataclass
from typing import Any

from moviedb.core.db import models


@dataclass(frozen=True)
class EntitySpec:
    name: str  # singular, used in error messages
    path: str  # REST collection path
    model: type
    seed: dict[str, Any]  # kwargs for the row inserted as id=1
    expected: dict[str, Any]  # expected REST representation of that row
    repo_module: str
    repo_class: str
    service_module: str
    service_class: str
    domain_module: str
    domain_class: str
    prerequisites: tuple[tuple[type, dict[str, Any]], ...] = ()


def _spec(name, path, module, model, cls, seed, expected, prerequisites=()):
    return EntitySpec(
        name=name,
        path=path,
        model=model,
        seed=seed,
        expected=expected,
        repo_module=f"moviedb.core.repositories.{module}",
        repo_class=f"{cls}Repository",
        service_module=f"moviedb.core.services.{module}",
        service_class=f"{cls}Service",
        domain_module=f"moviedb.core.domain.{module}",
        domain_class=cls,
        prerequisites=prerequisites,
    )


READ_ONLY_ENTITIES = [
    _spec(
        "director",
        "directors",
        "directors",
        models.Director,
        "Director",
        {"first_name": "Greta", "last_name": "Gerwig"},
        {"id": 1, "first_name": "Greta", "last_name": "Gerwig"},
    ),
    _spec(
        "mpaa_rating",
        "mpaa-ratings",
        "mpaa_ratings",
        models.MpaaRating,
        "MpaaRating",
        {"code": "PG", "description": "Parental Guidance"},
        {"id": 1, "code": "PG", "description": "Parental Guidance"},
    ),
    _spec(
        "genre",
        "genres",
        "genres",
        models.Genre,
        "Genre",
        {"name": "Drama"},
        {"id": 1, "name": "Drama"},
    ),
    _spec(
        "company",
        "companies",
        "companies",
        models.Company,
        "Company",
        {"name": "A24"},
        {"id": 1, "name": "A24"},
    ),
    _spec(
        "review",
        "reviews",
        "reviews",
        models.Review,
        "Review",
        {"movie_id": 1, "reviewer": "Sam", "rating": 5, "body": "Great"},
        {"id": 1, "movie_id": 1, "reviewer": "Sam", "rating": 5, "body": "Great"},
        prerequisites=((models.Movie, {"title": "Prereq"}),),
    ),
]
