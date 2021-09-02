import re


def bool_parser(value) -> bool:
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


def float_parser(value) -> float:
    if isinstance(value, (int, float)):
        return value
    elif isinstance(value, str):
        if re.match(r"^[\d]{0,}.?[\d]{1,}?$", value):
            return float(value)
    try:
        return float(value)
    finally:
        return None


def int_parser(value) -> int:
    value = float_parser(value)
    if value:
        value = int(value)
    return value
