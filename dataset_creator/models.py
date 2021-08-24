from typing import List

from pydantic import BaseModel, Field, validator

from utils import convert_timestamp_format


class CreateDatasetBody(BaseModel):
    sensors: List[str] = Field(
        ...,
        title="List of sensors name",
        min_items=1,
        description=(
            "At least 1 sensor must be specified. Sensor name must be "
            "represented in 'name_N' format, where N is number from 0 to 4."
        ),
    )
    start_timestamp: str = Field(
        ...,
        min_length=19,
        max_length=19,
        title="Start timestamp data",
        description=(
            "The string representation of the timestamp must not be 19 "
            "characters longer and must be in format 'H:M:S d.m.Y'"
        ),
    )
    end_timestamp: str = Field(
        ...,
        min_length=19,
        max_length=19,
        title="End timestamp data",
        description=(
            "The string representation of the timestamp must not be 19 "
            "characters longer and must be in format 'H:M:S d.m.Y'"
        ),
    )

    @validator("sensors")
    def sensors_validator(cls, v):
        if len(set(v)) != len(v):
            raise ValueError("List of sensors contain dublicate values")
        for value in v:
            splitted = value.split("_")
            if len(splitted) != 2:
                raise ValueError(f"Bad format of value {value}")
            if not splitted[0].isalpha() or not splitted[1].isnumeric():
                raise ValueError(f"Bad format of value {value}")
        return v

    @validator("start_timestamp")
    def start_timestamp_validator(cls, v):
        try:
            v = convert_timestamp_format(v)
        except ValueError:
            raise ValueError(f"Bad format of timestamp '{v}'")
        return v

    @validator("end_timestamp")
    def end_timestamp_validator(cls, v):
        try:
            v = convert_timestamp_format(v)
        except ValueError:
            raise ValueError(f"Bad format of timestamp '{v}'")
        return v

    class Config:
        schema_extra = {
            "example": {
                "sensors": ["alpha_1", "beta_2", "gamma_3"],
                "start_timestamp": "12:00:00 10.08.2018",
                "end_timestamp": "23:00:00 10.08.2018",
            }
        }


class CreateDatasetResponse(BaseModel):
    message: str
    file_path: str


class CreateDatasetError(BaseModel):
    message: str
    status_code: int
    details: dict
