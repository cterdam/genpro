"""Update the logger with runtime configs."""

import sys
from typing import List

from src.config.lab_config import LabConfig

__all__ = [
    "update_logger",
]


def update_logger(logger, config: LabConfig) -> List[str]:
    """Update the logger with runtime configs.

    This func should be called by config scaffold, as a setup step for the configs.

    Args:
        logger (Logger): A loguru logger
        config (LabConfig)

    Returns (List[str]):
        A list of msgs about the logging setup to be logged by its caller. If the stdout
        sink is not configured, also prints them to stdout.
    """

    ###################################################################################
    # Constants

    log_format = "\n".join(
        [
            "<dim>" + "=" * 88,
            "{file.path}:{line} <{function}>",
            "<level>[{level}]</> {time:YYYY-MM-DD HH:mm:ss!UTC}",
            "-" * 88 + "</>",
            "<level>{message}</>",
            "",
        ]
    )

    log_level = 0

    ###################################################################################

    # Logging msgs to return
    msgs = []

    # Add stdout handler
    if config.log.to_stdout:
        logger.add(sys.stdout, format=log_format, level=log_level)

    # Add local file handler
    if config.log.to_file:
        file_path = config.log.local_dir / (config.general.run_name + ".log")
        logger.add(file_path, format=log_format, level=log_level)

        msgs.append(
            f"Log file at {config.log.local_dir / (config.general.run_name + '.log')}"
        )

    # Print msgs if stdout sink is not configured
    if not config.log.to_stdout:
        for msg in msgs:
            print(msg)

    # Return logging msgs for caller to log
    return msgs
