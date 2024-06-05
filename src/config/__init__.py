"""Load the config selection and export each module."""

from importlib.resources import files

from src.util import load_yaml_file

from .lab_config import LabConfig
from .lib import arg_update
from .lib import setup

__all__ = [
    "config",
]

default_selection_raw = load_yaml_file(files("src.config") / "select.yaml")
default_selection = {
    f"{key}_source": val
    for key, val in default_selection_raw.items()
}
default_config = LabConfig(**default_selection)
config = arg_update(default_config)
setup(config)
