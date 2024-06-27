# 🧑‍💻 Lab source code

## 🛠️ config

- The config includes a number of groups, each containing a number of options.
  - `python -m src -h` to see all configurable options.
- Each group is stored in a subdir of `src/config/groups/`. Within each such subdir:
  - Each group sets a schema in `lab_config_{group_name}.py`.
  - Any yaml file in `all/` satisfying its schema is a valid source.
  - The source name is the file's base name, without the `.yaml` extension.
- `src/config/select.yaml` selects a default source name for each group.
- Each option in each group necessarily has a value at runtime. These are decided with
  the [precedence](#precedence) of config values.
- At runtime, after command-line [parsing](#parsing), the `src.config` module exports an
  object, `config`, which is a `LabConfig` and contains the final value of all options.

### Precedence

Even though each config option necessarily has a value at runtime, all command line
arguments are optional. This is because these values can still come from other places.
In decreasing levels of precedence, these are:

- Run-time command-line argument `--<group_name>/<option_name> <value>`
  - **This has the highest precedence.**
  - All values are taken as strings and parsed into expected types in the same
    way `yaml` parses strings into Python objects. Therefore:
    - In order to set a value to `None`, the input string should be `null` or `Null`.
    - In order to force a numeric string to be string, the input string should be
      surrounded with quotation marks.
      - Depending on the shell, while invoking the script, an escape might be needed for
        the quotation marks to be interpreted as part of the string.
- Source selected via a command-line argument `--<group_name> <source_name>`
- Source selected in `src/config/select.yaml`
- Default value provided in the group's schema class
  - **This has the lowest precedence.**

### Parsing

- During argparse, each option is available as a command-line argument.
  - Any option not set via command-line arguments has the value of `None` in argparse,
    which is used to prevent it from overwriting the value taken from other sources.
  - This is different from the user-input string of `null`. So, by setting an option to
    `null`, users can still manually assign `None` to a config option.

- Config options are processed after parsing, a processed called scaffolding.
  - In this process, their values could change.
  - The config table exported via logging provide config values after scaffolding.
  - With `--dry-run`, configs are exported directly after parsing, without scaffolding.

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

## 🪵 log

- Logs will appear at a number of destinations by default:
  - Stdout
  - Local log file
    - The default destination is `lab/out/<project_name>/<run_name>.log`.
    - If an alternative local dir is configured, the destination is
      `<local_dir>/<run_name>.log`.

- To log msgs, simply `from src.log import logger` and use `logger` as in `loguru`.

## 🧮 data

## 📐 eval

## 🪆 model

## 🚂 train

## 🔗 util
