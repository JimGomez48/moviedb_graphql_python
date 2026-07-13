from collections.abc import Iterable
from typing import TypeVar

from fastapi import HTTPException, status
from sqlalchemy.orm import DeclarativeBase, Session

ModelType = TypeVar("ModelType", bound=DeclarativeBase)


def serialize_row(row: DeclarativeBase) -> dict[str, object]:
    """Return mapped column values without exposing SQLAlchemy internals."""
    return {column.key: getattr(row, column.key) for column in row.__table__.columns}


def serialize_rows(rows: Iterable[DeclarativeBase]) -> list[dict[str, object]]:
    return [serialize_row(row) for row in rows]


def get_row_or_404(
    session: Session, model: type[ModelType], entity_name: str, entity_id: int
) -> ModelType:
    row = session.get(model, entity_id)
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{entity_name} with id {entity_id} was not found",
        )
    return row
