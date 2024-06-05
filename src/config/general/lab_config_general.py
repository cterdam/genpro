"""Config about general experiment setup."""

from pydantic import Field
from src.config.lab_config_base import LabConfigBase

__all__ = [
    "LabConfigGeneral",
]


class LabConfigGeneral(LabConfigBase):
    """Config about general experiment setup."""

    project_name: str = Field(description="Name of the current project.")
