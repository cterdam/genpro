"""Config for random states."""

import os
from typing import Literal

from pydantic import Field

from src.config.lab_config_base import LabConfigBase
from src.util import multiline

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

    torch_backends_cudnn_benchmark: bool | None = Field(
        default=None,
        description=multiline(f"""
            False is deterministic.
            Check https://pytorch.org/docs/stable/notes/randomness.html
        """),
    )

    torch_use_deterministic_algorithms: bool | None = Field(
        default=None,
        description=multiline(f"""
            True is deterministic. Check
            {
                multiline('''
                    pytorch.org/docs/stable/generated/
                    torch.use_deterministic_algorithms.html
                ''', is_url=True)
            }
        """),
    )

    cublas_workspace_config: Literal[":16:8", ":4096:8"] | None = Field(
        default_factory=\
                lambda: os.environ.get("CUBLAS_WORKSPACE_CONFIG", None),
        description=multiline(f"""
            If set, cuBLAS will give deterministic behavior even with multiple
            concurrent streams sharing a single cuBLAS handle. Check
            {
                multiline('''
                    https://docs.nvidia.com/cuda/cublas/
                    index.html#results-reproducibility
                ''', is_url=True)
            }
        """),
    )
