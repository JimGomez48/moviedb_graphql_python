from collections.abc import Collection
from typing import Protocol

from pydantic import BaseModel
from sqlalchemy import func, inspect, select
from sqlalchemy.orm import DeclarativeBase, InstrumentedAttribute, Session

from moviedb.core.pagination import PageParams, PageResult

type IdColumn = InstrumentedAttribute[int] | InstrumentedAttribute[int | None]


class ReadRepository[ReadType](Protocol):
    """What services need from a repository, independent of the ORM model."""

    def list_page(self, params: PageParams) -> PageResult[ReadType]: ...

    def get(self, entity_id: int) -> ReadType | None: ...

    def get_many(self, entity_ids: Collection[int]) -> dict[int, ReadType]: ...


class Repository[
    ModelType: DeclarativeBase,
    ReadType: BaseModel,
    CreateType: BaseModel,
]:
    """Generic SQLAlchemy access that only ever hands back Pydantic schemas."""

    def __init__(
        self,
        session: Session,
        model: type[ModelType],
        read_schema: type[ReadType],
    ) -> None:
        self._session = session
        self._model = model
        self._read_schema = read_schema

    def list_page(self, params: PageParams) -> PageResult[ReadType]:
        total = self._session.scalar(select(func.count()).select_from(self._model))
        rows = self._session.scalars(
            select(self._model)
            .order_by(*inspect(self._model).primary_key)
            .offset(params.offset)
            .limit(params.size)
        )
        return PageResult(
            items=[self._read_schema.model_validate(row) for row in rows],
            total=total or 0,
            params=params,
        )

    def get(self, entity_id: int) -> ReadType | None:
        row = self._session.get(self._model, entity_id)
        if row is None:
            return None
        return self._read_schema.model_validate(row)

    def get_many(self, entity_ids: Collection[int]) -> dict[int, ReadType]:
        """Batch lookup keyed by id; ids that do not exist are simply absent."""
        if not entity_ids:
            return {}
        primary_key = inspect(self._model).primary_key[0]
        rows = self._session.scalars(
            select(self._model).where(primary_key.in_(entity_ids))
        )
        return {
            getattr(row, primary_key.key): self._read_schema.model_validate(row)
            for row in rows
        }

    def _grouped_by(
        self, column: IdColumn, owner_ids: Collection[int]
    ) -> dict[int, list[ReadType]]:
        """Rows whose foreign key `column` is in `owner_ids`, grouped by that key."""
        if not owner_ids:
            return {}
        rows = self._session.scalars(
            select(self._model)
            .where(column.in_(owner_ids))
            .order_by(*inspect(self._model).primary_key)
        )
        grouped: dict[int, list[ReadType]] = {}
        for row in rows:
            grouped.setdefault(getattr(row, column.key), []).append(
                self._read_schema.model_validate(row)
            )
        return grouped

    def _linked(
        self,
        target_column: InstrumentedAttribute[int],
        owner_column: InstrumentedAttribute[int],
        owner_ids: Collection[int],
    ) -> dict[int, list[ReadType]]:
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
        grouped: dict[int, list[ReadType]] = {}
        for owner_id, row in rows:
            grouped.setdefault(owner_id, []).append(
                self._read_schema.model_validate(row)
            )
        return grouped

    def create(self, data: CreateType) -> ReadType:
        row = self._model(**data.model_dump())
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return self._read_schema.model_validate(row)
