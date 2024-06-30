"""Update the logger with runtime configs."""

import os
import sys
from typing import List

from src.config.lab_config import LabConfig
from src.util import multiline

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

    # Allow all logs
    log_level = 0

    ###################################################################################

    # Collect logging msgs to return
    msgs = []

    # Add stdout handler
    if config.log.to_stdout:
        logger.add(sys.stdout, format=log_format, level=log_level)

        msgs.append("Logging to stdout.")

    # Add local file handler
    if config.log.to_file:
        file_path = config.general.out_dir / "log.txt"
        logger.add(file_path, format=log_format, level=log_level)

        msgs.append(f"Logging to file at {file_path}")

    # Add W&B handler
    if config.log.to_wandb:

        assert "WANDB_API_KEY" in os.environ
        import wandb

        # Use the latest version of W&B backend. See https://wandb.me/wandb-core
        wandb.require("core")

        # Suppress W&B logs
        os.environ["WANDB_SILENT"] = "true"

        # Create run
        wandb.init(
            project=config.general.project_name,
            name=config.general.run_name,
            id=config.general.run_name,
            dir=config.general.out_dir,
            config=config,
        )

        msgs.append(
            "Logging to wandb at "
            + multiline(
                f"""
                https://wandb.ai
                /{wandb.run.entity}
                /{wandb.run.project}
                /runs
                /{wandb.run.id}
                """,
                is_url=True,
            )
        )

    # Return logging msgs for caller to log
    if not config.log.to_stdout:
        for msg in msgs:
            print(msg)
    return msgs
