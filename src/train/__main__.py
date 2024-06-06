from src.config import config
import random

print(random.randint(1, 100))

from src.util import get_random_state_setter

setter = get_random_state_setter(config)

setter()
