"""Keyboard shortcut component."""

from typing import Any

from refast.components.base import Component


class KeyboardShortcut(Component):
    """
    An invisible component that captures keyboard shortcuts and triggers callbacks.

    Registers one or more keyboard shortcuts on the page. When a shortcut is
    pressed the corresponding server callback is invoked.

    When multiple ``KeyboardShortcut`` components on the same page register the
    same key combo:

    * The component with the **highest** ``priority`` value handles it first.
    * By default (``bubble=False``) no further components are notified once a
      handler fires.  Set ``bubble=True`` on a component to let the shortcut
      continue propagating to lower-priority components after its own callback
      runs.

    Shortcut strings use the format ``"modifier+key"``, e.g. ``"ctrl+k"``,
    ``"ctrl+shift+n"``, ``"alt+f"``, ``"meta+k"`` (⌘ on macOS).
    Modifier names are case-insensitive; the plain key should be a single
    character or a named key (``"enter"``, ``"escape"``, ``"arrowup"``, …).

    Example:
        ```python
        KeyboardShortcut(
            shortcuts={
                "ctrl+k": ctx.callback(open_search),
                "ctrl+shift+n": ctx.callback(new_item),
            },
            priority=10,
            bubble=False,
        )
        ```

    Args:
        shortcuts: Mapping of shortcut string → callback.  All shortcuts
            registered by this instance share the same ``priority`` and
            ``bubble`` settings.
        priority: Higher values are handled before lower values when multiple
            components register the same shortcut. Defaults to ``0``.
        bubble: When ``True``, after this component's callback runs the
            shortcut event continues propagating to other registered
            components (those with lower priority, or those that set
            ``bubble=True`` themselves). When ``False`` (default), propagation
            stops after this component fires. Defaults to ``False``.
        prevent_default: When ``True`` the browser's default action for the
            key combination is suppressed (e.g. prevents Ctrl+S from opening
            the browser save dialog). Defaults to ``True``.
        enabled: When ``False`` the shortcuts are temporarily disabled without
            removing the component from the tree. Defaults to ``True``.
    """

    component_type: str = "KeyboardShortcut"

    def __init__(
        self,
        shortcuts: dict[str, Any],
        priority: int = 0,
        bubble: bool = False,
        prevent_default: bool = True,
        enabled: bool = True,
        id: str | None = None,
        extra_props: dict[str, Any] | None = None,
    ):
        super().__init__(id=id, extra_props=extra_props)
        self.shortcuts = shortcuts
        self.priority = priority
        self.bubble = bubble
        self.prevent_default = prevent_default
        self.enabled = enabled

    def render(self) -> dict[str, Any]:
        serialized_shortcuts = {
            key: (cb.serialize() if hasattr(cb, "serialize") and callable(cb.serialize) else cb)
            for key, cb in self.shortcuts.items()
        }

        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "shortcuts": serialized_shortcuts,
                "priority": self.priority,
                "bubble": self.bubble,
                "prevent_default": self.prevent_default,
                "enabled": self.enabled,
                **self._serialize_extra_props(),
            },
            "children": [],
        }
