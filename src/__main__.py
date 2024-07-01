from .config import config
from .log import logger
import random

logger.info(f"Random number {random.randint(1, 100)} generated.")


# get job type and set in wandb init
# wandb handle log entries
