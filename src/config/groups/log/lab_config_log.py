"""Config about logging."""

from pydantic import Field

from src.config.lab_config_base import LabConfigBase

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
        description="If true, writes logs to a local file log.txt in out dir.",
    )

    to_wandb: bool = Field(
        default=True,
        description="If true, reports logs to wandb.",
    )
