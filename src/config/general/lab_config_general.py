"""Config for general run options."""

from pydantic import BaseModel
from pydantic import Field
from src.util import multiline

__all__ = [
    "LabConfigGeneral",
]


class LabConfigGeneral(BaseModel):

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
