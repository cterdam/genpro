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

    # Collecting msgs to be logged while logger is not set up
    msgs = []

    # Set up run name
    if config.general.use_run_identifier:
        config.general.run_name += "-" + get_unique_id()
        msgs.append("Appending unique identifier to run name.")

    # Set up logger
    if config.log.to_file:
        if config.log.local_dir is None:
            config.log.local_dir = (
                files("src") / ".." / "out" / config.general.project_name
            )
        config.log.local_dir = config.log.local_dir.resolve()
    msgs.extend(update_logger(logger, config))

    # Set up random state
    get_random_state_setter(config, logger)()

    # Log setup msgs and resultant configs
    logger.trace("\n".join(msgs))
    logger.info("Finished setting up all configs.\n" + str(config))
