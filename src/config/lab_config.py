"""Load & keep the config selected for each module."""

from importlib.resources import files
from typing import Any, List, Tuple

from prettytable import PrettyTable
from pydantic import Field, ValidationInfo, field_validator

from src.config.lab_config_base import LabConfigBase
from src.util import denonify, load_yaml_file

from .groups.general.lab_config_general import LabConfigGeneral
from .groups.random.lab_config_random import LabConfigRandom

__all__ = [
    "LabConfig",
]


class LabConfig(LabConfigBase):
    """Overall config, contains all config groups.

    Setting the `{group_name}_source` attr with a valid source name will auto load the
    corresponding yaml file into the `{group_name}` attr.
    """

    general_source: str
    general: LabConfigGeneral | None = Field(default=None)

    random_source: str
    random: LabConfigRandom | None = Field(default=None)

    @property
    def groups(self) -> List[Tuple[str, LabConfigBase]]:
        """Return config group names and objs in self, excluding source fields."""
        return [
            (group_name, getattr(self, group_name))
            for group_name in self.model_fields
            if "_source" not in group_name
        ]

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
        group_name = info.field_name.replace("_source", "")
        file_path = files(f"src.config.groups.{group_name}.all") / f"{val}.yaml"
        assert file_path.is_file(), f"Did not find file at {file_path}."
        return str(file_path)

    def __setattr__(self, name: str, value: Any, /) -> None:
        """If changing the source name of a group, load the corresponding config file"""
        super().__setattr__(name, value)
        if "_source" in name:
            group_name = name.replace("_source", "")
            group_class = denonify(self.__fields__[group_name].annotation)
            file_loc = vars(self)[name]
            vars(self)[group_name] = group_class(**load_yaml_file(file_loc))

    def __str__(self) -> str:
        """Print a pretty table."""

        table = PrettyTable()

        table.title = "Config"
        table.field_names = ["GROUP", "OPTION", "VALUE"]
        table.align = "l"

        for group_name, group_obj in self.groups:

            rows = [["", key, val] for key, val in group_obj.dict().items()]
            rows[0][0] = group_name
            last_row = rows.pop(-1)
            table.add_rows(rows)
            table.add_row(last_row, divider=True)

        return table.get_string()
