"""Load the config selection and export each module."""

from importlib.resources import files

from src.util import load_yaml_file

from .lab_config import LabConfig
from .lib import arg_update, setup

__all__ = [
    "config",
]

selections_raw = load_yaml_file(files("src.config") / "select.yaml")
selections = {f"{key}_source": val for key, val in selections_raw.items()}
config = LabConfig(**selections)
config = arg_update(config)
setup(config)
