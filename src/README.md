# 🧑‍💻 Lab source code

## 🛠️ config

- The config includes a number of components.
- Each component is stored in a subdir of `src/config/`.
  Within each such subdir:
  - Each component sets a schema in `lab_config_{component_name}.py`.
  - Any yaml file in `all/` satisfying its schema is a valid source.
  - The source name is the file's base name, without the `.yaml` extension.
- `src/config/select.yaml` appoints a source name for each component.
- The `src.config` module exports an object, `config`, which is a `LabConfig`
  and contains all components as chosen in `src/config/select.yaml`.

## 🗃️ data

## 📈 eval

## 🧠 model

## 🚂 train

## ⛓️ util
