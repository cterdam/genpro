"""Config about general experiment setup."""

from pydantic import Field

from src.config.lab_config_base import LabConfigBase
from src.util import multiline

__all__ = [
    "LabConfigGeneral",
]


class LabConfigGeneral(LabConfigBase):
    """Config about the general experiment setup."""

    project_name: str = Field(
        default="lab",
        description="Name of the current project.",
    )

    run_name: str = Field(
        default="run",
        description="Name of the current run.",
    )

    use_run_identifier: bool = Field(
        default=True,
        description=multiline(
            """
            If True, appends a unique identifier to the run name, including the
            username, timestamp, and a random hash.
            """
        ),
    )
