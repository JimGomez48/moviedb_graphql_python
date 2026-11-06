import importlib
from unittest.mock import create_autospec

import pytest

from moviedb.core.errors import NotFoundError
from tests.entities import READ_ONLY_ENTITIES, EntitySpec

ids = [spec.name for spec in READ_ONLY_ENTITIES]


def _load(spec: EntitySpec):
    repo = getattr(importlib.import_module(spec.repo_module), spec.repo_class)
    service = getattr(importlib.import_module(spec.service_module), spec.service_class)
    schema = getattr(importlib.import_module(spec.schema_module), spec.schema_class)
    return repo, service, schema


@pytest.mark.parametrize("spec", READ_ONLY_ENTITIES, ids=ids)
def test_get_returns_entity(spec: EntitySpec) -> None:
    # Arrange
    repo_cls, service_cls, schema_cls = _load(spec)
    repo = create_autospec(repo_cls, instance=True)
    entity = schema_cls(**spec.expected)
    repo.get.return_value = entity

    # Act
    result = service_cls(repo).get(1)

    # Assert
    assert result == entity


@pytest.mark.parametrize("spec", READ_ONLY_ENTITIES, ids=ids)
def test_get_raises_not_found(spec: EntitySpec) -> None:
    # Arrange
    repo_cls, service_cls, _ = _load(spec)
    repo = create_autospec(repo_cls, instance=True)
    repo.get.return_value = None

    # Act / Assert
    with pytest.raises(NotFoundError) as exc_info:
        service_cls(repo).get(5)
    assert str(exc_info.value) == f"{spec.name} with id 5 was not found"
