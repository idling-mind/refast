"""Button components."""

from typing import Any, Literal

from refast.components.base import Component, ChildrenType


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
        size: Literal["xs", "sm", "md", "lg", "xl"] = "md",
        icon: str | None = None,
        icon_position: Literal["left", "right"] = "left",
        disabled: bool = False,
        loading: bool = False,
        type: Literal["button", "submit", "reset"] = "button",
        on_click: Any = None,
        id: str | None = None,
        class_name: str = "",
        style: dict[str, Any] | None = None,
        parent_style: dict[str, Any] | None = None,
        extra_props: dict[str, Any] | None = None,
    ):
        super().__init__(
            id=id,
            class_name=class_name,
            style=style,
            parent_style=parent_style,
            extra_props=extra_props,
        )
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
        props: dict[str, Any] = {
            "variant": self.variant,
            "size": self.size,
            "disabled": self.disabled or self.loading,
            "loading": self.loading,
            "type": self.button_type,
            "icon": self.icon,
            "icon_position": self.icon_position,
            "class_name": self.class_name,
        }

        if self.on_click:
            props["on_click"] = self.on_click.serialize()

        props.update(self._serialize_extra_props())

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
        size: Literal["xs", "sm", "md", "lg", "xl"] = "md",
        disabled: bool = False,
        on_click: Any = None,
        aria_label: str | None = None,
        id: str | None = None,
        class_name: str = "",
        style: dict[str, Any] | None = None,
        parent_style: dict[str, Any] | None = None,
        extra_props: dict[str, Any] | None = None,
    ):
        super().__init__(
            id=id,
            class_name=class_name,
            style=style,
            parent_style=parent_style,
            extra_props=extra_props,
        )
        self.icon = icon
        self.variant = variant
        self.size = size
        self.disabled = disabled
        self.on_click = on_click
        self.aria_label = aria_label

    def render(self) -> dict[str, Any]:
        props: dict[str, Any] = {
            "icon": self.icon,
            "variant": self.variant,
            "size": self.size,
            "disabled": self.disabled,
            "aria_label": self.aria_label,
            "class_name": self.class_name,
        }

        if self.on_click:
            props["on_click"] = self.on_click.serialize()

        props.update(self._serialize_extra_props())

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": [],
        }


class ButtonGroup(Component):
    """
    A container that groups related buttons together with consistent styling.

    Example:
        ```python
        ButtonGroup(children=[
            Button("Button 1"),
            Button("Button 2"),
        ])
        ```

    Args:
        orientation: Layout orientation (``"horizontal"`` or ``"vertical"``).
    """

    component_type: str = "ButtonGroup"

    def __init__(
        self,
        children: ChildrenType = None,
        orientation: Literal["horizontal", "vertical"] = "horizontal",
        id: str | None = None,
        class_name: str = "",
        style: dict[str, Any] | None = None,
        parent_style: dict[str, Any] | None = None,
        extra_props: dict[str, Any] | None = None,
    ):
        super().__init__(
            id=id,
            class_name=class_name,
            style=style,
            parent_style=parent_style,
            extra_props=extra_props,
        )
        self.orientation = orientation
        self.add_children(children)

    def render(self) -> dict[str, Any]:
        props = {
            "orientation": self.orientation,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }
        self._validate_props(props)
        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": self._render_children(),
        }


class ButtonGroupSeparator(Component):
    """
    The ButtonGroupSeparator component visually divides buttons within a group.

    Example:
        ```python
        ButtonGroup(children=[
            Button("Button 1"),
            ButtonGroupSeparator(),
            Button("Button 2"),
        ])
        ```

    Args:
        orientation: Layout orientation (``"horizontal"`` or ``"vertical"``).
    """

    component_type: str = "ButtonGroupSeparator"

    def __init__(
        self,
        orientation: Literal["horizontal", "vertical"] = "vertical",
        id: str | None = None,
        class_name: str = "",
        style: dict[str, Any] | None = None,
        parent_style: dict[str, Any] | None = None,
        extra_props: dict[str, Any] | None = None,
    ):
        super().__init__(
            id=id,
            class_name=class_name,
            style=style,
            parent_style=parent_style,
            extra_props=extra_props,
        )
        self.orientation = orientation

    def render(self) -> dict[str, Any]:
        props = {
            "orientation": self.orientation,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }
        self._validate_props(props)
        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": [],
        }


class ButtonGroupText(Component):
    """
    Use this component to display text within a button group.

    Example:
        ```python
        ButtonGroup(children=[
            ButtonGroupText("Text"),
            Button("Button"),
        ])
        ```

    Args:
        text: The text to render.
        as_child: Whether to render as a child component (e.g. Label).
    """

    component_type: str = "ButtonGroupText"

    def __init__(
        self,
        text: str | None = None,
        as_child: bool = False,
        children: ChildrenType = None,
        id: str | None = None,
        class_name: str = "",
        style: dict[str, Any] | None = None,
        parent_style: dict[str, Any] | None = None,
        extra_props: dict[str, Any] | None = None,
    ):
        super().__init__(
            id=id,
            class_name=class_name,
            style=style,
            parent_style=parent_style,
            extra_props=extra_props,
        )
        self.as_child = as_child
        if text is not None:
            self.add_children(text)
        if children is not None:
            self.add_children(children)

    def render(self) -> dict[str, Any]:
        props = {
            "as_child": self.as_child,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }
        self._validate_props(props)
        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": self._render_children(),
        }
