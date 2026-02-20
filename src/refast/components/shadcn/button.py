"""Button components."""

from typing import Any, Literal

from refast.components.base import Component


class Button(Component):
    """
    Button component based on shadcn.

    Example:
        ```python
        # Basic button
        Button(
            "Click Me",
            variant="primary",
            on_click=ctx.callback(handle_click)
        )

        # Button with icon
        Button(
            "Save",
            icon="save",
            on_click=ctx.callback(handle_save)
        )

        # Button with icon on right
        Button(
            "Next",
            icon="arrow-right",
            icon_position="right",
            on_click=ctx.callback(handle_next)
        )
        ```

    Args:
        label: The button text
        variant: Button style variant
        size: Button size
        icon: Optional Lucide icon name (e.g., "save", "home", "settings")
        icon_position: Position of the icon relative to label ("left" or "right")
        disabled: Whether the button is disabled
        loading: Whether to show loading spinner
        type: HTML button type
        on_click: Click callback
    """

    component_type: str = "Button"

    def __init__(
        self,
        label: str,
        variant: Literal[
            "default", "primary", "secondary", "destructive", "outline", "ghost", "link"
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
    """Button with just an icon."""

    component_type: str = "IconButton"

    def __init__(
        self,
        icon: str,
        variant: Literal[
            "default", "primary", "secondary", "destructive", "outline", "ghost"
        ] = "ghost",
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
