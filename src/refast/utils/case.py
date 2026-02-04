"""
Case conversion utilities for Refast.

Naming Convention Architecture:
------------------------------
- **Python (Backend)**: All user-facing APIs use snake_case (PEP 8)
- **TypeScript (Frontend)**: All user-facing APIs use camelCase (JavaScript convention)
- **Wire Format (Props)**: snake_case - frontend ComponentRenderer converts to camelCase
- **Wire Format (Internal)**: camelCase for non-prop fields (callbackId, sessionId, etc.)

The conversion boundary is at ComponentRenderer.tsx which uses snakeToCamel()
for all prop keys received from Python.

This module provides utilities for case conversion when needed, but most
conversions happen automatically at the frontend boundary.
"""

import re
from typing import Any


def snake_to_camel(snake_str: str) -> str:
    """
    Convert snake_case string to camelCase.

    Args:
        snake_str: A snake_case string (e.g., "my_variable_name")

    Returns:
        A camelCase string (e.g., "myVariableName")

    Examples:
        >>> snake_to_camel("hello_world")
        'helloWorld'
        >>> snake_to_camel("on_click")
        'onClick'
        >>> snake_to_camel("already")
        'already'
        >>> snake_to_camel("_private")
        '_private'
        >>> snake_to_camel("html_id")
        'htmlId'
    """
    if not snake_str or "_" not in snake_str:
        return snake_str

    # Handle leading underscores (preserve them)
    leading_underscores = len(snake_str) - len(snake_str.lstrip("_"))
    prefix = snake_str[:leading_underscores]
    rest = snake_str[leading_underscores:]

    if not rest:
        return snake_str

    components = rest.split("_")
    # First component stays lowercase, rest get title-cased
    result = components[0] + "".join(x.title() for x in components[1:] if x)
    return prefix + result


def camel_to_snake(camel_str: str) -> str:
    """
    Convert camelCase string to snake_case.

    Args:
        camel_str: A camelCase string (e.g., "myVariableName")

    Returns:
        A snake_case string (e.g., "my_variable_name")

    Examples:
        >>> camel_to_snake("helloWorld")
        'hello_world'
        >>> camel_to_snake("onClick")
        'on_click'
        >>> camel_to_snake("already")
        'already'
        >>> camel_to_snake("HTMLParser")
        'html_parser'
        >>> camel_to_snake("getHTTPResponse")
        'get_http_response'
    """
    if not camel_str:
        return camel_str

    # Insert underscore before uppercase letters that follow lowercase letters
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", camel_str)
    # Insert underscore before uppercase letters that are followed by lowercase
    result = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)
    return result.lower()


def convert_keys_to_camel(
    data: dict[str, Any],
    recursive: bool = True,
    exclude_keys: set[str] | None = None,
) -> dict[str, Any]:
    """
    Convert all dictionary keys from snake_case to camelCase.

    Args:
        data: Dictionary with snake_case keys
        recursive: If True, recursively convert nested dictionaries and lists
        exclude_keys: Set of keys to skip conversion for

    Returns:
        New dictionary with camelCase keys

    Examples:
        >>> convert_keys_to_camel({"my_key": "value", "other_key": 123})
        {'myKey': 'value', 'otherKey': 123}
        >>> convert_keys_to_camel({"nested": {"inner_key": 1}})
        {'nested': {'innerKey': 1}}
    """
    exclude = exclude_keys or set()
    result = {}

    for key, value in data.items():
        new_key = key if key in exclude else snake_to_camel(key)

        if recursive:
            value = _convert_value_keys(value, snake_to_camel, True, exclude)

        result[new_key] = value

    return result


def convert_keys_to_snake(
    data: dict[str, Any],
    recursive: bool = True,
    exclude_keys: set[str] | None = None,
) -> dict[str, Any]:
    """
    Convert all dictionary keys from camelCase to snake_case.

    Args:
        data: Dictionary with camelCase keys
        recursive: If True, recursively convert nested dictionaries and lists
        exclude_keys: Set of keys to skip conversion for

    Returns:
        New dictionary with snake_case keys

    Examples:
        >>> convert_keys_to_snake({"myKey": "value", "otherKey": 123})
        {'my_key': 'value', 'other_key': 123}
        >>> convert_keys_to_snake({"nested": {"innerKey": 1}})
        {'nested': {'inner_key': 1}}
    """
    exclude = exclude_keys or set()
    result = {}

    for key, value in data.items():
        new_key = key if key in exclude else camel_to_snake(key)

        if recursive:
            value = _convert_value_keys(value, camel_to_snake, True, exclude)

        result[new_key] = value

    return result


def _convert_value_keys(
    value: Any,
    converter: callable,
    recursive: bool,
    exclude_keys: set[str],
) -> Any:
    """
    Recursively convert keys in nested structures.

    Args:
        value: The value to process
        converter: The key conversion function to use
        recursive: Whether to process nested structures
        exclude_keys: Keys to exclude from conversion

    Returns:
        The value with converted keys (if applicable)
    """
    if isinstance(value, dict):
        result = {}
        for k, v in value.items():
            new_key = k if k in exclude_keys else converter(k)
            if recursive:
                v = _convert_value_keys(v, converter, True, exclude_keys)
            result[new_key] = v
        return result
    elif isinstance(value, list):
        return [_convert_value_keys(item, converter, recursive, exclude_keys) for item in value]
    else:
        return value


def validate_snake_case(key: str) -> bool:
    """
    Check if a string is valid snake_case.

    Args:
        key: The string to validate

    Returns:
        True if the string is snake_case, False otherwise

    Examples:
        >>> validate_snake_case("hello_world")
        True
        >>> validate_snake_case("helloWorld")
        False
        >>> validate_snake_case("_private_var")
        True
        >>> validate_snake_case("CONSTANT")
        False
    """
    if not key:
        return False
    # Allow leading underscores, then lowercase letters, digits, and underscores
    # No consecutive underscores, no trailing underscore (unless single char)
    pattern = r"^_*[a-z][a-z0-9]*(_[a-z0-9]+)*$"
    return bool(re.match(pattern, key))


def has_camel_case_keys(data: dict[str, Any]) -> list[str]:
    """
    Find any camelCase keys in a dictionary (for validation/debugging).

    Args:
        data: Dictionary to check

    Returns:
        List of keys that appear to be camelCase

    Examples:
        >>> has_camel_case_keys({"snake_case": 1, "camelCase": 2})
        ['camelCase']
    """
    camel_keys = []
    for key in data.keys():
        # A key is camelCase if it has uppercase letters (not at start) and no underscores
        if "_" not in key and re.search(r"[a-z][A-Z]", key):
            camel_keys.append(key)
    return camel_keys
