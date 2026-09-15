from pydantic import BaseModel, ConfigDict


class MpaaRatingBase(BaseModel):
    code: str
    description: str | None = None


class MpaaRatingCreate(MpaaRatingBase):
    pass


class MpaaRatingRead(MpaaRatingBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
