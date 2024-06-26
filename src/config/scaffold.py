"""Various pre-processing steps for config options after parsing."""

from src.util import get_random_state_setter

from .lab_config import LabConfig

__all__ = [
    "scaffold",
]


def scaffold(config: LabConfig):
    """Process config options that require setup."""

    # Set up random state
    get_random_state_setter(config)()
