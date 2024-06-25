"""Various pre- and pro- processing routines with config args."""

import argparse

from src.util import get_random_state_setter
from src.util import get_type_name
from src.util import load_yaml_var
from src.util import multiline

from .lab_config import LabConfig

__all__ = [
    "arg_update",
    "setup",
]


def arg_update(config: LabConfig) -> LabConfig:
    """Update a LabConfig with command-line argument selections."""

    parser = argparse.ArgumentParser(
        prog="PROG",
        usage="%(prog)s (--<opt_name> <opt_value>)*",
        description=multiline(
            """
            All opt values optional. Values are taken as strings and parsed into
            expected types in the same way `yaml` parses strings into Python
            objects.
            """
        ),
    )

    # Add dry run option
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="show all configured option values and exit",
    )

    # Arg group for selecting alternative sources for each group
    sources_group = parser.add_argument_group(
        title="sources",
        description="Load alternative sources for config defaults.",
    )

    # Add options from each config group
    for group_name in config.model_fields:

        if "_source" in group_name:
            # Not a config group object
            continue

        sources_group.add_argument(
            f"--{group_name}",
            metavar=f"[str]",
            required=False,
            type=str,
            help=f"Source name for the {group_name} config group.",
        )

        this_config_group = getattr(config, group_name)

        # Arg group for this config group
        this_arg_group = parser.add_argument_group(
            title=group_name,
            description=type(this_config_group).model_json_schema()["description"],
        )

        for field_name, field_info in this_config_group.model_fields.items():
            this_arg_group.add_argument(
                f"--{group_name}/{field_name}",
                metavar=f"[{get_type_name(field_info.annotation)}]",
                required=False,
                type=str,
                help=field_info.description,
            )

    # Unset options are mapped to the value of None
    args_dict = vars(parser.parse_args())

    # Load alternative sources for groups
    for group_name in config.model_fields:
        if "_source" in group_name:
            continue
        if args_dict[group_name] is not None:
            setattr(
                config,
                f"{group_name}_source",
                args_dict[group_name],
            )

    # Load each set option
    for arg_name, arg_val in args_dict.items():
        if "/" not in arg_name or arg_val is None:
            continue
        group_name, opt_name = arg_name.split("/", 1)
        setattr(
            getattr(config, group_name),
            opt_name,
            load_yaml_var(arg_val),
        )

    # If dry run, print all configs to stdout and exit
    if args_dict["dry_run"]:
        print(config)
        parser.exit()

    return config


def setup(config: LabConfig):
    """Process config options that require setup."""

    # Set up random state
    get_random_state_setter(config)()
