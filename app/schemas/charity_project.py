from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from app.core.constants import MAX_LEN_NAME, MIN_LEN_DESCRIPTION, MIN_LEN_NAME


class CharityProjectBase(BaseModel):
    name: str = Field(
        ...,
        min_length=MIN_LEN_NAME,
        max_length=MAX_LEN_NAME
    )
    description: str = Field(..., min_length=MIN_LEN_DESCRIPTION)
    full_amount: PositiveInt

    model_config = ConfigDict(extra='forbid')


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(BaseModel):
    name: str | None = Field(
        None,
        min_length=MIN_LEN_NAME,
        max_length=MAX_LEN_NAME
    )
    description: str | None = Field(None, min_length=MIN_LEN_DESCRIPTION)
    full_amount: PositiveInt | None = None

    model_config = ConfigDict(extra='forbid')


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True,
        extra='forbid',
    )
