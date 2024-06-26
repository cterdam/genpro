"""Prepare the default logger, not configured with custom logging options."""

from loguru import logger

__all__ = [
    "get_logger",
]


def get_logger():
    """Prepare the logger."""

    # Remove default stderr handler
    logger.remove()

    # Make default info level not bold
    logger.level("INFO", color=logger.level("INFO").color.replace("<bold>", ""))

    return logger
