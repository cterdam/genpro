"""Base class for config classes."""

from pydantic import BaseModel
from pydantic import ConfigDict

__all__ = [
    "LabConfigBase",
]


class LabConfigBase(BaseModel):

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )
