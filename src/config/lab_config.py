"""Load & keep the config selected for each module."""

from importlib.resources import files
from typing import Any

from pydantic import Field
from pydantic import field_validator
from pydantic import ValidationInfo
from src.config.lab_config_base import LabConfigBase
from src.util import load_yaml_file

from .general.lab_config_general import LabConfigGeneral
from .random.lab_config_random import LabConfigRandom

__all__ = [
    "LabConfig",
]


class LabConfig(LabConfigBase):
    """Overall config, contains all components.

    Setting the `{component_name}_source` attr with a valid source name will
    auto load the corresponding yaml file into the `{component_name}` attr.
    """

    general_source: str
    general: LabConfigGeneral | None = Field(default=None)

    random_source: str
    random: LabConfigRandom | None = Field(default=None)

    def __init__(self, /, **data: Any) -> None:
        """Perform init and load each config file needed."""
        super().__init__(**data)
        self.general = LabConfigGeneral(**load_yaml_file(self.general_source))
        self.random = LabConfigRandom(**load_yaml_file(self.random_source))

    @field_validator(
        "general_source",
        "random_source",
    )
    @classmethod
    def expand_path(cls, val: str, info: ValidationInfo) -> str:
        """Convert a source name to the corresponding yaml file path."""
        dirname = info.field_name.replace("_source", "")
        filename = files(f"src.config.{dirname}.all") / f"{val}.yaml"
        assert filename.is_file(), f"Did not find file at {filename}."
        return filename

    def __setattr__(self, name: str, value: Any, /) -> None:
        """Reload config file if a source name is updated."""
        super().__setattr__(name, value)
        # If changing the source of a component, reload the config file
        if "_source" in name:
            target_name = name.replace("_source", "")
            target_class = self.__fields__[target_name].annotation
            file_loc = vars(self)[name]
            vars(self)[target_name] = target_class(**load_yaml_file(file_loc))
