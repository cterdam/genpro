"""Config about logging."""

from pydantic import Field

from src.config.lab_config_base import LabConfigBase
from src.util.general import multiline

__all__ = [
    "LabConfigWandb",
]


class LabConfigWandb(LabConfigBase):
    """Config about W&B."""

    entity: str | None = Field(
        default=None,
        description=multiline(
            """
            Username or team name for wandb. If unset, will be default entity associated
            with login.
            """
        ),
    )

    save_code: bool = Field(
        default=True,
        description="If true, saves all .py source code files in repo on wandb.",
    )
