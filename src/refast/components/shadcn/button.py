"""Button components."""

from typing import Any, Literal

from refast.components.base import Component


class Button(Component):
    """
    Button component based on shadcn.

    Example:
        ```python
        Button(
            "Click Me",
            variant="primary",
            on_click=ctx.callback(handle_click)
        )
        ```
    """

    component_type: str = "Button"

    def __init__(
        self,
        label: str,
        variant: Literal[
            "default", "primary", "secondary", "destructive", "outline", "ghost", "link"
        ] = "default",
        size: Literal["sm", "md", "lg", "icon"] = "md",
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
        self.disabled = disabled
        self.loading = loading
        self.button_type = type
        self.on_click = on_click

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "variant": self.variant,
                "size": self.size,
                "disabled": self.disabled or self.loading,
                "loading": self.loading,
                "type": self.button_type,
                "onClick": self.on_click.serialize() if self.on_click else None,
                "className": self.class_name,
                **self.extra_props,
            },
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
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "icon": self.icon,
                "variant": self.variant,
                "size": self.size,
                "disabled": self.disabled,
                "onClick": self.on_click.serialize() if self.on_click else None,
                "ariaLabel": self.aria_label,
                "className": self.class_name,
                **self.extra_props,
            },
            "children": [],
        }
