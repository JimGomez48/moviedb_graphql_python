from typing import Protocol

from pydantic import BaseModel
from sqlalchemy import func, inspect, select
from sqlalchemy.orm import DeclarativeBase, Session

from moviedb.core.pagination import PageParams, PageResult

class ReadRepository[ReadType](Protocol):
    """What services need from a repository, independent of the ORM model."""

    def list_page(self, params: PageParams) -> PageResult[ReadType]: ...

    def get(self, entity_id: int) -> ReadType | None: ...


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

    def create(self, data: CreateType) -> ReadType:
        row = self._model(**data.model_dump())
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return self._read_schema.model_validate(row)
