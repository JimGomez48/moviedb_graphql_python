import dataclasses
import importlib

import pytest
from sqlalchemy.orm import Session

from moviedb.core.pagination import PageParams
from tests.entities import READ_ONLY_ENTITIES, EntitySpec
from tests.helpers import seed_entity

ids = [spec.name for spec in READ_ONLY_ENTITIES]


def _load(spec: EntitySpec):
    repo = getattr(importlib.import_module(spec.repo_module), spec.repo_class)
    domain = getattr(importlib.import_module(spec.domain_module), spec.domain_class)
    return repo, domain


@pytest.mark.parametrize("spec", READ_ONLY_ENTITIES, ids=ids)
def test_get_returns_domain_model_never_orm_model(
    session: Session, spec: EntitySpec
) -> None:
    # Arrange
    repo_cls, domain_cls = _load(spec)
    seed_entity(session, spec)

    # Act
    found = repo_cls(session).get(1)

    # Assert
    assert isinstance(found, domain_cls)
    assert dataclasses.asdict(found) == spec.expected


@pytest.mark.parametrize("spec", READ_ONLY_ENTITIES, ids=ids)
def test_get_returns_none_when_missing(session: Session, spec: EntitySpec) -> None:
    # Arrange
    repo_cls, _ = _load(spec)

    # Act / Assert
    assert repo_cls(session).get(999) is None


@pytest.mark.parametrize("spec", READ_ONLY_ENTITIES, ids=ids)
def test_list_page_returns_domain_models(session: Session, spec: EntitySpec) -> None:
    # Arrange
    repo_cls, domain_cls = _load(spec)
    seed_entity(session, spec, count=2)

    # Act
    page = repo_cls(session).list_page(PageParams(page=1, size=10))

    # Assert
    assert page.total == 2
    assert all(isinstance(item, domain_cls) for item in page.items)
