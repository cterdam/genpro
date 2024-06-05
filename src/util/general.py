from datetime import datetime
import getpass
import textwrap
from types import NoneType
from types import UnionType
from typing import Any, get_args
import uuid

from yaml import safe_load

__all__ = [
    "get_unique_id",
    "multiline",
    "load_yaml_file",
    "load_yaml_var",
    "get_type_name",
    "denonify",
]


def get_unique_id() -> str:
    """Prepare a unique identifier for a run."""
    _username: str = getpass.getuser()
    _datetime: str = datetime.now().strftime("%Y%m%d-%Hh%Mm%Ss")
    _hashdigits: int = 4
    _randhash: str = uuid.uuid4().hex[-_hashdigits:]
    unique_id: str = f"{_username}-{_datetime}-{_randhash}"
    return unique_id


def multiline(s: str) -> str:
    """Correctly connect a multiline string.

    Args:
        s (str): A string, usually formed with three double quotes.

    Returns:
        str: A string formed by removing all common whitespaces near the start
        of each line in the original string.
    """
    return textwrap.dedent(s).replace("\n", " ").strip()


def load_yaml_file(filepath) -> dict:
    with open(filepath) as f:
        result = safe_load(f)
    return result


def load_yaml_var(v: str) -> Any:
    """Given a string, interpret it as a variable using yaml's load logic."""
    return safe_load(f"key: {v}")["key"]


def get_type_name(t: type | UnionType) -> str:
    """Given a type or a union type, infer the class name in str."""
    return str(t) if isinstance(t, UnionType) else t.__name__


def denonify(ut: UnionType) -> type:
    """Given an optional type, return the non-None base type(s) in it."""
    union_args = get_args(ut)
    non_none_types = [arg for arg in union_args if arg is not NoneType]
    if len(non_none_types) == 1:
        return non_none_types[0]
    elif len(non_none_types) > 1:
        return Union[tuple(non_none_types)]
