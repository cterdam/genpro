"""Base class for all config group classes."""

from pydantic import BaseModel
from pydantic import ConfigDict

__all__ = [
    "LabConfigBase",
]


class LabConfigBase(BaseModel):

    model_config = ConfigDict(
        validate_default=True,
        validate_assignment=True,
        extra="forbid",
    )
