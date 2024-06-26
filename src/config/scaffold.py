"""Various pre-processing steps for config options after parsing."""

from src.util import get_random_state_setter, get_unique_id

from .lab_config import LabConfig

__all__ = [
    "scaffold",
]


def scaffold(config: LabConfig):
    """Process config options that require setup."""

    # Set up run name
    if config.general.use_run_identifier:
        config.general.run_name += "-" + get_unique_id()

    # Set up random state
    get_random_state_setter(config)()
