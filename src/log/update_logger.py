"""Update the logger with runtime configs."""

import sys

from src.config.lab_config import LabConfig

__all__ = [
    "update_logger",
]


def update_logger(logger, config: LabConfig):
    """Update the logger with runtime configs.

    The logger already starts logging in this function. However, since the setup is
    incremental, at each log entry, it only logs to components set up at that point.
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

    # Add stdout handler
    if config.log.to_stdout:
        logger.add(sys.stdout, format=log_format, level=log_level)

    # Add local file handler
    if config.log.to_file:
        file_path = config.log.local_dir / (config.general.run_name + ".log")
        logger.add(file_path, format=log_format, level=log_level)

        file_msg = (
            f"Log file at {config.log.local_dir / (config.general.run_name + '.log')}"
        )
        logger.trace(file_msg)
        if not config.log.to_stdout:
            print(file_msg)
