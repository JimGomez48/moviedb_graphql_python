from sqlalchemy.orm import Session

from tests.entities import EntitySpec


def seed_entity(session: Session, spec: EntitySpec, count: int = 1) -> None:
    """Insert prerequisites plus `count` rows of the entity (first one has id=1)."""
    for model, kwargs in spec.prerequisites:
        session.add(model(**kwargs))
    session.flush()
    for index in range(count):
        # Suffix strings after the first row so unique columns don't collide.
        suffix = f"-{index}" if index else ""
        session.add(
            spec.model(
                **{
                    key: f"{value}{suffix}" if isinstance(value, str) else value
                    for key, value in spec.seed.items()
                }
            )
        )
    session.commit()
