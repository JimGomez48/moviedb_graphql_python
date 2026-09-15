from pydantic import BaseModel, ConfigDict


class ReviewBase(BaseModel):
    movie_id: int
    reviewer: str | None = None
    rating: int | None = None
    body: str | None = None


class ReviewCreate(ReviewBase):
    pass


class ReviewRead(ReviewBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
