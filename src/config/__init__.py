"""Load the config selection and export each module."""

from importlib.resources import files

from src.util import load_yaml

from .config import Config

__all__ = [
    "config",
]

select_raw = load_yaml(files("src.config") / "select.yaml")
select = {f"{key}_file": val for key, val in select_raw.items()}

config = Config(**select)
