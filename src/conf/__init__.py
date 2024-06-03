"""Load the config selection and export each module."""

from importlib.resources import files

from src.util import load_yaml

from .lab_config import LabConfig

__all__ = [
    "config",
]

select_raw = load_yaml(files("src.conf") / "select.yaml")
select = {f"{key}_file": val for key, val in select_raw.items()}

config = LabConfig(**select)
