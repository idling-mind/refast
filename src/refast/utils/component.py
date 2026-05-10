"""Component utility functions."""

from collections.abc import Callable

from refast.components.base import Component


def walk(root: Component, visitor: Callable[[Component], None]) -> None:
    """Call *visitor* on *root* and every descendant, depth-first.

    Traversal follows :meth:`~refast.components.base.Component._traversal_children`
    so that component-type-specific children (e.g. ``Slot.fallback``) are
    included without any special-casing here.

    Args:
        root: The root of the component subtree to walk.
        visitor: Callable invoked once for every :class:`Component` encountered.
    """
    visitor(root)
    for child in root._traversal_children():
        walk(child, visitor)


def find(root: Component, target_id: str) -> Component | None:
    """Return the first component in the tree whose ``id`` equals *target_id*.

    Uses :meth:`~refast.components.base.Component._traversal_children` for
    traversal, so component-specific children (e.g. ``Slot.fallback``) are
    searched automatically.

    Args:
        root: The root of the component subtree to search.
        target_id: The ``id`` to look for.

    Returns:
        The matching component, or ``None`` if not found.
    """
    if root.id == target_id:
        return root
    for child in root._traversal_children():
        found = find(child, target_id)
        if found:
            return found
    return None


def find_component_in_tree(root: Component, target_id: str) -> Component | None:
    """Alias for :func:`find`; kept for backward compatibility."""
    return find(root, target_id)
