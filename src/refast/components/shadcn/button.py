"""Button components."""

from typing import Any, Literal

from refast.components.base import Component


class Button(Component):
    """
    A clickable button component based on shadcn/ui.

    Example:
        ```python
        # Basic button
        Button("Click Me", on_click=ctx.callback(handle_click))

        # Destructive button with icon
        Button("Delete", variant="destructive", icon="trash", on_click=ctx.callback(handle_delete))

        # Ghost button with right-aligned icon
        Button("Next", variant="ghost", icon="arrow-right", icon_position="right")

        # Submit button in a form
        Button("Save", variant="default", size="lg", type="submit")
        ```

    Args:
        label: The button text.
        variant: Visual style. ``"default"`` is the primary filled style.
        size: Button size. ``"icon"`` renders a square icon-only button.
        icon: Optional Lucide icon name (e.g. ``"save"``, ``"trash"``).
        icon_position: Whether the icon appears before or after the label.
        disabled: Prevents interaction when ``True``.
        loading: Shows a spinner and sets ``disabled`` when ``True``.
        type: HTML ``<button>`` type attribute.
        on_click: Server callback invoked on click.
    """

    component_type: str = "Button"

    def __init__(
        self,
        label: str,
        variant: Literal[
            "default", "secondary", "destructive", "outline", "ghost", "link"
        ] = "default",
        size: Literal["sm", "md", "lg", "icon"] = "md",
        icon: str | None = None,
        icon_position: Literal["left", "right"] = "left",
        disabled: bool = False,
        loading: bool = False,
        type: Literal["button", "submit", "reset"] = "button",
        on_click: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.label = label
        self.variant = variant
        self.size = size
        self.icon = icon
        self.icon_position = icon_position
        self.disabled = disabled
        self.loading = loading
        self.button_type = type
        self.on_click = on_click

    def render(self) -> dict[str, Any]:
        props = {
            "variant": self.variant,
            "size": self.size,
            "disabled": self.disabled or self.loading,
            "loading": self.loading,
            "type": self.button_type,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.icon:
            props["icon"] = self.icon
            props["icon_position"] = self.icon_position

        if self.on_click:
            props["on_click"] = self.on_click.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": [self.label],
        }


class IconButton(Component):
    """
    An icon-only button, rendered as a square.

    Example:
        ```python
        IconButton(icon="trash", aria_label="Delete item", on_click=ctx.callback(handle_delete))
        IconButton(icon="settings", variant="outline", size="lg")
        ```

    Args:
        icon: Lucide icon name (e.g. ``"trash"``, ``"edit"``, ``"settings"``).
        variant: Visual style variant.
        size: Button size (controls icon size as well).
        disabled: Prevents interaction when ``True``.
        aria_label: Accessible label — defaults to the icon name if omitted.
        on_click: Server callback invoked on click.
    """

    component_type: str = "IconButton"

    def __init__(
        self,
        icon: str,
        variant: Literal["default", "secondary", "destructive", "outline", "ghost"] = "ghost",
        size: Literal["sm", "md", "lg"] = "md",
        disabled: bool = False,
        on_click: Any = None,
        aria_label: str | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.icon = icon
        self.variant = variant
        self.size = size
        self.disabled = disabled
        self.on_click = on_click
        self.aria_label = aria_label

    def render(self) -> dict[str, Any]:
        props = {
            "icon": self.icon,
            "variant": self.variant,
            "size": self.size,
            "disabled": self.disabled,
            "aria_label": self.aria_label,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.on_click:
            props["on_click"] = self.on_click.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": [],
        }
