# 🧑‍💻 Lab source code

## 🛠️ config

- The config includes a number of components, each containing a number of
  options.
- Each option in each component will necessarily have a value at runtime. These
  are decided with
  [the precedence of config values](#the-precedence-of-config-values).
- Each component is stored in a subdir of `src/config/`.
  Within each such subdir:
  - Each component sets a schema in `lab_config_{component_name}.py`.
  - Any yaml file in `all/` satisfying its schema is a valid source.
  - The source name is the file's base name, without the `.yaml` extension.
- `src/config/select.yaml` selects a source name for each component.
- At runtime, the `src.config` module exports an object, `config`, which is a
  `LabConfig` and contains the final value of all options.

### The precedence of config values

A config value for an option can potentially come from a lot of places. In
decreasing levels of precedence, these are:

- Run-time command-line argument `--<component_name>/<option_name> <value>`
  - All values are taken as strings and parsed into expected types in the same
    way `yaml` parses strings into Python objects.
  - **This has the highest precedence.**
- Source selected in a command-line argument `--<component_name> <source_name>`
- Source selected in `src/config/select.yaml`
- Default value provided in component schema class
  - **This has the lowest precedence.**

### Adding a new component

- Make the subdir `src/config/<new_comp_name>`. In it:
  - `lab_config_<new_comp_name>.py` defines the schema.
    - This needs to subclass `LabConfigBase`.
  - `all/` contains at least one yaml file which satisfies the schema.
    - There should be a `default.yaml` which just writes `{}`, so it uses the
      default value for all options.
- In `src/config/lab_config.py`, modify `LabConfig`.
  - Add the `<new_comp_name>` field.
  - Add the `<new_comp_name_source>` field.
    - Register it to the field validator `expand_path`.
  - Modify the `__init__` method to initialize the `<new_comp_name>` field.
- Modify `select.yaml` to select a source for this new component.

And that's it!

### Adding a new option within an existent component

- Modify the component schema to register the new option as a field.
  - Provide a meaningfully restrictive type, a default value, and a description.
- If this value necessitates postprocessing, modify `src/config/lib.py/setup`.

And that's it!

## 🧮 data

## 📐 eval

## 🪆 model

## 🚂 train

## 🔗 util
