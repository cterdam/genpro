"""Config for random states."""

from pydantic import Field

from src.config.lab_config_base import LabConfigBase

__all__ = [
    "LabConfigRandom",
]


class LabConfigRandom(LabConfigBase):
    """Config about random states."""

    python_seed: int | None = Field(
        default=None,
        description=("Seed for Python's built-in random module."),
    )

    numpy_seed: int | None = Field(
        default=None,
        description=("Seed for Numpy."),
    )

    torch_seed: int | None = Field(
        default=None,
        description=("Seed for PyTorch for both CPU and GPU."),
    )
