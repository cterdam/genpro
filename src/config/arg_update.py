"""Update a LabConfig with argparse selections."""

import argparse

from .lab_config import LabConfig

__all__ = [
    "arg_update",
]


def arg_update(config: LabConfig) -> LabConfig:
    """Update a LabConfig with command-line argument selections."""

    parser = argparse.ArgumentParser()

    for component_name in config.model_fields_set:

        if "_source" in component_name:
            # Source file name, not config component instance
            continue

        component = getattr(config, component_name)
        component_doc = component.__class__.model_json_schema()["description"]

        # Add argument group for each config component
        this_group = parser.add_argument_group(
            title=component_name,
            description=component_doc,
        )

        # Add each option in component as command-line arg in group
        for field_name, field_info in component.__fields__.items():

            arg_name = f"--{component_name}/{field_name}"
            arg_help = field_info.description
            arg_type = field_info.annotation

            this_group.add_argument(
                arg_name,
                metavar=field_name.upper(),
                required=False,
                type=str,
                help=arg_help,
            )

    args = parser.parse_args()

    return config

    # add load file options

    # When parsing is done, first load relevant files for defaults

    # Then, args that are not None are input by user
    # Parse these one by one to load into config
