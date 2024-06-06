from datetime import datetime
import getpass
import os
import random
import textwrap
from types import NoneType
from types import UnionType
from typing import _UnionGenericAlias, Any, Callable, get_args
import uuid

from yaml import safe_load

__all__ = [
    "get_unique_id",
    "multiline",
    "load_yaml_file",
    "load_yaml_var",
    "get_type_name",
    "denonify",
    "get_random_state_setter",
]


def get_unique_id() -> str:
    """Prepare a unique identifier for a run."""
    _username: str = getpass.getuser()
    _datetime: str = datetime.now().strftime("%Y%m%d-%Hh%Mm%Ss")
    _hashdigits: int = 4
    _randhash: str = uuid.uuid4().hex[-_hashdigits:]
    unique_id: str = f"{_username}-{_datetime}-{_randhash}"
    return unique_id


def multiline(s: str, is_url: bool = False) -> str:
    """Correctly connect a multiline string.

    Args:
        s (str): A string, usually formed with three double quotes.

    Returns:
        str: A string formed by removing all common whitespaces near the start
        of each line in the original string.
    """
    result = textwrap.dedent(s).replace("\n", " ").strip()
    if is_url:
        result = result.replace(" ", "")
    return result


def load_yaml_file(filepath) -> dict:
    with open(filepath) as f:
        result = safe_load(f)
    return result


def load_yaml_var(v: str) -> Any:
    """Given a string, interpret it as a variable using yaml's load logic."""
    return safe_load(f"key: {v}")["key"]


def get_type_name(t: type | UnionType) -> str:
    """Given a type or a union type, infer the class name in str."""
    if isinstance(t, UnionType) or isinstance(t, _UnionGenericAlias):
        # UnionType -> int | None
        # _UnionGenericAlias -> typing.Optional[int]
        return str(t)
    else:
        return t.__name__


def denonify(ut: UnionType) -> type:
    """Given an optional type, return the non-None base type(s) in it."""
    union_args = get_args(ut)
    non_none_types = [arg for arg in union_args if arg is not NoneType]
    if len(non_none_types) == 1:
        return non_none_types[0]
    elif len(non_none_types) > 1:
        return Union[tuple(non_none_types)]


def get_random_state_setter(config) -> Callable[[], None]:
    """Given the lab config, return a function that sets the random state.

    Arguments:
        config (LabConfig)

    Returns (Callable[[], None]):
        A function that sets the various random state according to the config.
    """

    # Lazy import on time-consuming imports
    torch_args = (config.random.torch_seed,
                  config.random.torch_backends_cudnn_benchmark,
                  config.random.torch_use_deterministic_algorithms)
    if any([optval is not None for optval in torch_args]):
        import torch

    if config.random.numpy_seed is not None:
        import numpy as np

    def random_state_setter():

        # Set each option
        if config.random.python_seed is not None:
            random.seed(config.random.python_seed)
        if config.random.numpy_seed is not None:
            np.random.seed(config.random.numpy_seed)
        if config.random.torch_seed is not None:
            torch.manual_seed(config.random.torch_seed)
        if config.random.torch_backends_cudnn_benchmark is not None:
            torch.backends.cudnn.benchmark = \
                    config.random.torch_backends_cudnn_benchmark
        if config.random.torch_use_deterministic_algorithms is not None:
            torch.use_deterministic_algorithms(
                config.random.torch_use_deterministic_algorithms)
        if config.random.cublas_workspace_config is not None:
            os.environ['CUBLAS_WORKSPACE_CONFIG'] = \
                    config.random.cublas_workspace_config

    return random_state_setter
