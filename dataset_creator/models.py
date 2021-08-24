from pydantic import BaseModel, Field
from typing import Optional, List


class CreateDatasetBody(BaseModel):
    sensors: List[str] = Field(
        ...,
        min_items=1,
        max_items=5,
        description="At least 1 sensor must be specified but no more then 5"
    )
    start_timestamp: str = Field(
        ...,
        min_length=19,
        max_length=19,
        description=(
            "The string representation of the timestamp must not be 19 "
            "characters longer"
        )
    )
    end_timestamp: str


class CreateDatasetResponse(BaseModel):
    message: str
    file_path: str


