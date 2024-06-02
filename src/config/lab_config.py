"""Load the config selected for each module."""

from importlib.resources import files
from typing import Self

from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator
from pydantic import model_validator
from pydantic import ValidationInfo
from src.util import load_yaml

from .general.lab_config_general import LabConfigGeneral

__all__ = [
    "LabConfig",
]


class LabConfig(BaseModel):

    general_file: str
    general: LabConfigGeneral = Field(default=None)

    @field_validator("general_file")
    @classmethod
    def expand_path(cls, val: str, info: ValidationInfo) -> str:
        dirname = info.field_name.replace("_file", "")
        return files(f"src.config.{dirname}.all") / f"{val}.yaml"

    @model_validator(mode="after")
    def load_configs(self) -> Self:
        self.general = LabConfigGeneral(**load_yaml(self.general_file))
        return self
