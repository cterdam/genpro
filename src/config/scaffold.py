"""Various pre-processing steps for config options after parsing."""

from importlib.resources import files

from src.log import logger, update_logger
from src.util import get_random_state_setter, get_unique_id

from .lab_config import LabConfig

__all__ = [
    "scaffold",
]


def scaffold(config: LabConfig):
    """Process config options that require setup."""

    # Collect msgs to be logged while logger is not set up
    msgs = ["Beginning run."]

    # Set up run name
    if config.general.run_identifier:
        config.general.run_name += "-" + get_unique_id()
        msgs.append("Appending unique identifier to run name.")

    # Set up out dir
    if config.general.out_dir is None:
        config.general.out_dir = (
            files("src")
            / ".."
            / "out"
            / config.general.project_name
            / config.general.run_name
        )
    config.general.out_dir = config.general.out_dir.resolve()
    msgs.append(f"Out dir set to {config.general.out_dir}")

    # Set up logger
    msgs.extend(update_logger(logger, config))

    # Logger is set up, release all msgs so far
    logger.trace("\n".join(msgs))

    # Set up random state
    get_random_state_setter(config, logger)()

    # Log setup msgs and resultant configs
    logger.info("Finished setting up all configs.\n" + str(config))
