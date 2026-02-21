"""Component utility functions."""
from typing import Optional
from refast.components.base import Component


def find_component_in_tree(root: Component, target_id: str) -> Optional[Component]:
    """
    Recursively find a component with the given ID in the component tree.

    Args:
        root: The root component to start searching from
        target_id: The ID of the component to find

    Returns:
        The component if found, None otherwise
    """
    if root.id == target_id:
        return root

    # Check children
    # Access private _children as this is a framework utility
    children = getattr(root, "_children", [])

    for child in children:
        if isinstance(child, Component):
            found = find_component_in_tree(child, target_id)
            if found:
                return found

    # Special handling for fallback components in Slots (and potentially others)
    # Using getattr to allow duck typing and avoid importing specific component classes
    # like Slot to prevent circular imports if those components eventually use utils
    fallback = getattr(root, "fallback", None)
    if isinstance(fallback, Component):
        found = find_component_in_tree(fallback, target_id)
        if found:
            return found

    return None
