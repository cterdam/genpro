from .config import config
from .log import logger
import random

logger.info(f"Random number {random.randint(1, 100)} generated.")


# wandb handle incremental log entries

# For wandb tables see:
# https://github.com/wandb/wandb/issues/2981#issuecomment-1686868189
