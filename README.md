# 💈 Lab

Lab (**L**anguage **A**I **B**uilding) allows you to systematically manage many
runs of training and evaluation of language models.

## 🏁 Setup

```zsh
conda create -n lab python=3.12
conda activate lab
pip install -r requirements.txt
```

## 🕹️ Use 

- `python -m src.train` to directly start using the default configs.
  - Add `-h` to see all configurable options.
  - Add `--dry-run` to print out configured option values and exit.
- By default, a log file will be created at `lab/out/<project_name>/<run_name>.log`.


## TODO

- save logs upon exit - use `atexit`
- compute SHA256 sum of each model and write a file when uploading
