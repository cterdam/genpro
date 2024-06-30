from .config import config
from .log import logger
import random

logger.info(f"Random number {random.randint(1, 100)} generated.")


# validate run name CANNOT CONTAIN /\#?%:
# get job type and set in wandb init

# wandb upload config
# wandb save code
