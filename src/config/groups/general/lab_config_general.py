"""Config about general experiment setup."""

from pathlib import Path
from typing import Literal

from pydantic import Field

from src.config.lab_config_base import LabConfigBase
from src.util import get_non_special_regex, multiline

__all__ = [
    "LabConfigGeneral",
]


class LabConfigGeneral(LabConfigBase):
    """Config about the general experiment setup."""

    project_name: str = Field(
        default="lab",
        description="Name of the current project. Cannot contain special characters.",
        pattern=get_non_special_regex(),
    )

    run_name: str = Field(
        default="run",
        description="Name of the current run. Cannot contain special characters.",
        pattern=get_non_special_regex(),
    )

    run_identifier: bool = Field(
        default=True,
        description=multiline(
            """
            If true, appends a unique identifier to the run name, including the
            username, the UTC timestamp, and a random hash.
            """
        ),
    )

    out_dir: Path | None = Field(
        default=None,
        description=multiline(
            """
            Directory to host any outputs of this run, including logs. Notation is
            relative to lauching command. Will be created (with any parent dirs) if
            non-existent. If None, defaults to (from repo root)
            `out/<project_name>/<run_name>`.
            """
        ),
    )

    task: Literal["debug", "train", "eval"] = Field(
        default="debug",
        description=multiline(
            """
            Task to perform. [train] Train a model. [eval] Eval a model. [debug] For
            debugging purposes, do nothing.
            """
        ),
    )
