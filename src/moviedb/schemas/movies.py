from pydantic import BaseModel, ConfigDict


class MovieBase(BaseModel):
    title: str
    release_year: int | None = None
    mpaa_rating_id: int | None = None


class MovieCreate(MovieBase):
    pass


class MovieRead(MovieBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
