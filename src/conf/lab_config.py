"""Load the config selected for each module."""

from importlib.resources import files
from typing import Any

from pydantic import Field
from pydantic import field_validator
from pydantic import ValidationInfo
from src.conf.lab_config_base import LabConfigBase
from src.util import load_yaml

from .general.lab_config_general import LabConfigGeneral

__all__ = [
    "LabConfig",
]


class LabConfig(LabConfigBase):

    general_file: str
    general: LabConfigGeneral = Field(default=None)

    @field_validator("general_file")
    @classmethod
    def expand_path(cls, val: str, info: ValidationInfo) -> str:
        dirname = info.field_name.replace("_file", "")
        filename = files(f"src.conf.{dirname}.all") / f"{val}.yaml"
        assert filename.is_file(), f"Did not find file at {filename}."
        return filename

    def __init__(self, /, **data: Any) -> None:
        """Do the init and load config files."""
        super().__init__(**data)
        self.general = LabConfigGeneral(**load_yaml(self.general_file))

    def __setattr__(self, name: str, value: Any, /) -> None:
        """Reload config file if a filename is updated."""
        super().__setattr__(name, value)
        if name == "general_file":
            self.general = LabConfigGeneral(**load_yaml(self.general_file))
