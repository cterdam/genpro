"""Update a LabConfig with argparse selections."""

import argparse

from src.util import get_type_name
from src.util import load_yaml_var

from .lab_config import LabConfig

__all__ = [
    "arg_update",
]


def arg_update(config: LabConfig) -> LabConfig:
    """Update a LabConfig with command-line argument selections."""

    parser = argparse.ArgumentParser()

    # Arg group for appointing alternative sources for components
    sources_group = parser.add_argument_group(
        title="sources",
        description="Load alternative sources for config defaults.",
    )

    # Add options within each component
    for component_name in config.model_fields:

        if "_source" in component_name:
            continue

        sources_group.add_argument(
            f"--{component_name}",
            metavar=f"[str]",
            required=False,
            type=str,
            help=f"Source name for the {component_name} config component.",
        )

        component = getattr(config, component_name)

        # Arg group for each component
        this_group = parser.add_argument_group(
            title=component_name,
            description=type(component).model_json_schema()["description"],
        )

        for field_name, field_info in component.model_fields.items():
            this_group.add_argument(
                f"--{component_name}/{field_name}",
                metavar=f"[{get_type_name(field_info.annotation)}]",
                required=False,
                type=str,
                help=field_info.description,
            )

    # Unset options are mapped to the value of None
    args_dict = vars(parser.parse_args())

    # Load alternative sources for components
    for component_name in config.model_fields_set:
        if "_source" in component_name:
            continue
        if args_dict[component_name] is not None:
            setattr(
                config,
                f"{component_name}_source",
                args_dict[component_name],
            )
        del args_dict[component_name]

    # Load each option in components
    for arg_name, arg_val in args_dict.items():
        if arg_val is None:
            continue
        component_name, attr_name = arg_name.split("/", 1)
        setattr(
            getattr(config, component_name),
            attr_name,
            load_yaml_var(arg_val),
        )

    return config
