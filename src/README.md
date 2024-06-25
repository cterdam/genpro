# 🧑‍💻 Lab source code

## 🛠️ config

- The config includes a number of groups, each containing a number of options.
- Each option in each group will necessarily have a value at runtime. These
  are decided with
  [the precedence of config values](#the-precedence-of-config-values).
- Each group is stored in a subdir of `src/config/groups/`.
  Within each such subdir:
  - Each group sets a schema in `lab_config_{group_name}.py`.
  - Any yaml file in `all/` satisfying its schema is a valid source.
  - The source name is the file's base name, without the `.yaml` extension.
- `src/config/select.yaml` selects a source name for each group.
- At runtime, the `src.config` module exports an object, `config`, which is a
  `LabConfig` and contains the final value of all options.

### The precedence of config values

A config value for an option can potentially come from a lot of places. In
decreasing levels of precedence, these are:

- Run-time command-line argument `--<group_name>/<option_name> <value>`
  - All values are taken as strings and parsed into expected types in the same
    way `yaml` parses strings into Python objects.
  - **This has the highest precedence.**
- Source selected in a command-line argument `--<group_name> <source_name>`
- Source selected in `src/config/select.yaml`
- Default value provided in the group's schema class
  - **This has the lowest precedence.**

### Adding a new group

- Make the subdir `src/config/groups/<new_group_name>`. In it:
  - `lab_config_<new_group_name>.py` should define the schema.
    - This needs to subclass `LabConfigBase`.
  - `all/` contains at least one yaml file which satisfies the schema.
    - There should be a `default.yaml` which just writes `{}`, so it uses the
      default value set in the schema for all options.
- In `src/config/lab_config.py`, modify `LabConfig`.
  - Add the `<new_group_name>` field.
  - Add the `<new_group_name>_source` field.
    - Register it to the field validator for the `expand_path` method.
  - Modify the `__init__` method to initialize the `<new_group_name>` field.
- Modify `src/config/select.yaml` to select a source for this new group.

And that's it!

### Adding a new option within an existent group

- Modify the group schema to add the new option as a field.
  - If it can only take a few values, use `Literal` as its type.
  - If this is a shell variable, its default factory should fetch it from shell.
- If this value necessitates postprocessing, modify `src/config/lib.py/setup`.

And that's it!

## 🧮 data

## 📐 eval

## 🪆 model

## 🚂 train

## 🔗 util
