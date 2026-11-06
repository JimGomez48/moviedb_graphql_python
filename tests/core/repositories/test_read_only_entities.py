import importlib

import pytest
from sqlalchemy.orm import Session

from moviedb.core.pagination import PageParams
from tests.entities import READ_ONLY_ENTITIES, EntitySpec
from tests.helpers import seed_entity

ids = [spec.name for spec in READ_ONLY_ENTITIES]


def _load(spec: EntitySpec):
    repo = getattr(importlib.import_module(spec.repo_module), spec.repo_class)
    schema = getattr(importlib.import_module(spec.schema_module), spec.schema_class)
    return repo, schema


@pytest.mark.parametrize("spec", READ_ONLY_ENTITIES, ids=ids)
def test_get_returns_schema_never_orm_model(session: Session, spec: EntitySpec) -> None:
    # Arrange
    repo_cls, schema_cls = _load(spec)
    seed_entity(session, spec)

    # Act
    found = repo_cls(session).get(1)

    # Assert
    assert isinstance(found, schema_cls)
    assert found.model_dump() == spec.expected


@pytest.mark.parametrize("spec", READ_ONLY_ENTITIES, ids=ids)
def test_get_returns_none_when_missing(session: Session, spec: EntitySpec) -> None:
    # Arrange
    repo_cls, _ = _load(spec)

    # Act / Assert
    assert repo_cls(session).get(999) is None


@pytest.mark.parametrize("spec", READ_ONLY_ENTITIES, ids=ids)
def test_list_page_returns_schemas(session: Session, spec: EntitySpec) -> None:
    # Arrange
    repo_cls, schema_cls = _load(spec)
    seed_entity(session, spec, count=2)

    # Act
    page = repo_cls(session).list_page(PageParams(page=1, size=10))

    # Assert
    assert page.total == 2
    assert all(isinstance(item, schema_cls) for item in page.items)
