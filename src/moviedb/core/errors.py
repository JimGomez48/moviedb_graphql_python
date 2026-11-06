class NotFoundError(Exception):
    """Raised when a requested entity does not exist."""

    def __init__(self, entity_name: str, entity_id: int) -> None:
        super().__init__(f"{entity_name} with id {entity_id} was not found")
        self.entity_name = entity_name
        self.entity_id = entity_id
