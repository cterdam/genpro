"""Config for general run options."""

from pydantic import BaseModel
from pydantic import Field

from src.config.lab_config_base import LabConfigBase
from src.util import multiline

__all__ = [
    "LabConfigGeneral",
]


class LabConfigGeneral(LabConfigBase):
    """Config about the general experiment setup."""

    project_name: str = Field(description="Name of the current project.")

    python_seed: int | None = Field(
        default=None,
        description=("Python's built-in random seed."),
    )
    numpy_seed: int | None = Field(
        default=None,
        description=("Numpy random seed."),
    )
    torch_seed: int | None = Field(
        default=None,
        description=("PyTorch random seed for both CPU and GPU."),
    )
