"""Config about general experiment setup."""

from pathlib import Path
from types import NoneType

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

    run_identifier: bool = Field(
        default=True,
        description=multiline(
            """
            If True, appends a unique identifier to the run name, including the
            username, the UTC timestamp, and a random hash.
            """
        ),
    )

    out_dir: Path | NoneType = Field(
        default=None,
        description=multiline(
            """
            Directory to host any outputs of this run, including logs. Notation is
            relative to lauching command. Will be created (with any parent dirs) if
            non-existent. If None, Defaults to (repo root)
            `lab/out/<project_name>/<run_name>`.
            """
        ),
    )
