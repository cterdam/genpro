"""Load the config selection and export each module."""

from importlib.resources import files

from src.util import load_yaml

from .lab_config import LabConfig

__all__ = [
    "config",
]

select_raw = load_yaml(files("src.config") / "select.yaml")
select = {f"{key}_source": val for key, val in select_raw.items()}

config = LabConfig(**select)
