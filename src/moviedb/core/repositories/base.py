import dataclasses
from collections.abc import Callable, Collection
from typing import TYPE_CHECKING, Protocol

from sqlalchemy import func, inspect, select
from sqlalchemy.orm import DeclarativeBase, InstrumentedAttribute, Session

from moviedb.core.pagination import PageParams, PageResult

if TYPE_CHECKING:
    from _typeshed import DataclassInstance

type IdColumn = InstrumentedAttribute[int] | InstrumentedAttribute[int | None]


class ReadRepository[DomainType](Protocol):
    """What services need from a repository, independent of the ORM model."""

    def list_page(self, params: PageParams) -> PageResult[DomainType]: ...

    def get(self, entity_id: int) -> DomainType | None: ...

    def get_many(self, entity_ids: Collection[int]) -> dict[int, DomainType]: ...


class Repository[
    ModelType: DeclarativeBase,
    DomainType,
    NewType: DataclassInstance,
]:
    """Generic SQLAlchemy access that only ever hands back domain models."""

    def __init__(
        self,
        session: Session,
        model: type[ModelType],
        to_domain: Callable[[ModelType], DomainType],
    ) -> None:
        self._session = session
        self._model = model
        self._to_domain = to_domain

    def list_page(self, params: PageParams) -> PageResult[DomainType]:
        total = self._session.scalar(select(func.count()).select_from(self._model))
        rows = self._session.scalars(
            select(self._model)
            .order_by(*inspect(self._model).primary_key)
            .offset(params.offset)
            .limit(params.size)
        )
        return PageResult(
            items=[self._to_domain(row) for row in rows],
            total=total or 0,
            params=params,
        )

    def get(self, entity_id: int) -> DomainType | None:
        row = self._session.get(self._model, entity_id)
        if row is None:
            return None
        return self._to_domain(row)

    def get_many(self, entity_ids: Collection[int]) -> dict[int, DomainType]:
        """Batch lookup keyed by id; ids that do not exist are simply absent."""
        if not entity_ids:
            return {}
        primary_key = inspect(self._model).primary_key[0]
        rows = self._session.scalars(
            select(self._model).where(primary_key.in_(entity_ids))
        )
        return {getattr(row, primary_key.key): self._to_domain(row) for row in rows}

    def _grouped_by(
        self, column: IdColumn, owner_ids: Collection[int]
    ) -> dict[int, list[DomainType]]:
        """Rows whose foreign key `column` is in `owner_ids`, grouped by that key."""
        if not owner_ids:
            return {}
        rows = self._session.scalars(
            select(self._model)
            .where(column.in_(owner_ids))
            .order_by(*inspect(self._model).primary_key)
        )
        grouped: dict[int, list[DomainType]] = {}
        for row in rows:
            grouped.setdefault(getattr(row, column.key), []).append(
                self._to_domain(row)
            )
        return grouped

    def _linked(
        self,
        target_column: InstrumentedAttribute[int],
        owner_column: InstrumentedAttribute[int],
        owner_ids: Collection[int],
    ) -> dict[int, list[DomainType]]:
        """Rows of this entity reached through a join table, grouped by owner id.

        `target_column` is the join table column pointing at this entity and
        `owner_column` the one pointing at the entity the caller started from.
        """
        if not owner_ids:
            return {}
        link = target_column.class_
        primary_key = inspect(self._model).primary_key[0]
        rows = self._session.execute(
            select(owner_column, self._model)
            .select_from(link)
            .join(self._model, primary_key == target_column)
            .where(owner_column.in_(owner_ids))
            .order_by(link.id)
        )
        grouped: dict[int, list[DomainType]] = {}
        for owner_id, row in rows:
            grouped.setdefault(owner_id, []).append(self._to_domain(row))
        return grouped

    def create(self, data: NewType) -> DomainType:
        row = self._model(**dataclasses.asdict(data))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return self._to_domain(row)
