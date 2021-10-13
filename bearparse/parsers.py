import re
from typing import Any, Optional


def bool_parser(value: Any) -> bool:
    """Parse the value as a boolean.

    Args:
        value (Any): Value to parse as a boolean

    Returns:
        bool: Boolean result
    """
    if isinstance(value, bool):
        return value
    elif isinstance(value, (int, float)):
        return bool(value)
    elif isinstance(value, str):
        if value.lower() in ["y", "yes", "t", "true"]:
            return True
        elif re.match(r"^[\d]{0,}.?[\d]{1,}?$", value):
            return bool(float(value))
        else:
            print(value)
            return False


def float_parser(value: Any) -> Optional[float]:
    """Parse the value as a float.

    Args:
        value (Any): Value to parse as a float

    Returns:
        float | None: Float result, or None if value is not a float
    """
    if isinstance(value, (int, float)):
        return value
    elif isinstance(value, str):
        if re.match(r"^[\d]{0,}.?[\d]{1,}?$", value):
            return float(value)
    try:
        return float(value)
    finally:
        return None


def int_parser(value: Any) -> Optional[int]:
    """Parse the value as a int.

    Args:
        value (Any): Value to parse as a int

    Returns:
        int | None: Int result, or None if value is not a int
    """
    value = float_parser(value)
    if value:
        value = int(value)
    return value
