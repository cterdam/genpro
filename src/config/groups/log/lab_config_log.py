"""Config about logging."""

from pathlib import Path
from types import NoneType

from pydantic import Field

from src.config.lab_config_base import LabConfigBase
from src.util import multiline

__all__ = [
    "LabConfigLog",
]


class LabConfigLog(LabConfigBase):
    """Config about logging."""

    to_stdout: bool = Field(
        default=True,
        description="If true, prints logs to stdout.",
    )

    to_file: bool = Field(
        default=True,
        description="If true, writes logs to a local file <run_name>.log.",
    )

    local_dir: Path | NoneType = Field(
        default=None,
        description=multiline(
            """
            Parent directory of any local log file created. Defaults to
            `lab/log/<project_name>`.
            """
        ),
    )
