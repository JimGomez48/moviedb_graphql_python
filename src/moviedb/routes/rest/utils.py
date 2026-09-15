from fastapi import HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, Session


def paginate_rows[ModelType: DeclarativeBase, SchemaType: BaseModel](
    session: Session, model: type[ModelType], schema: type[SchemaType]
) -> Page[SchemaType]:
    return paginate(
        session,
        select(model).order_by(model.id),
        transformer=lambda rows: [schema.model_validate(row) for row in rows],
    )


def get_row_or_404[ModelType: DeclarativeBase](
    session: Session, model: type[ModelType], entity_name: str, entity_id: int
) -> ModelType:
    row = session.get(model, entity_id)
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{entity_name} with id {entity_id} was not found",
        )
    return row
