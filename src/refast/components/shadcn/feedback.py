"""Feedback components based on shadcn."""

from typing import Any, Literal

from refast.components.base import Component


class Alert(Component):
    """
    Alert component for displaying messages.

    Example:
        ```python
        Alert(
            title="Error",
            message="Something went wrong",
            variant="destructive"
        )
        ```
    """

    component_type: str = "Alert"

    def __init__(
        self,
        title: str | None = None,
        message: str | None = None,
        variant: Literal["default", "success", "warning", "destructive", "info"] = "default",
        dismissible: bool = False,
        on_dismiss: Any = None,
        children: list[Component | str] | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children
        self.title = title
        self.message = message
        self.variant = variant
        self.dismissible = dismissible
        self.on_dismiss = on_dismiss

    def render(self) -> dict[str, Any]:
        props = {
            "title": self.title,
            "message": self.message,
            "variant": self.variant,
            "dismissible": self.dismissible,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.on_dismiss:
            props["on_dismiss"] = self.on_dismiss.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": self._render_children(),
        }


class Spinner(Component):
    """Loading spinner component."""

    component_type: str = "Spinner"

    def __init__(
        self,
        size: Literal["sm", "md", "lg"] = "md",
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.size = size

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "size": self.size,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [],
        }


class Progress(Component):
    """Progress bar component."""

    component_type: str = "Progress"

    def __init__(
        self,
        value: int = 0,
        max: int = 100,
        label: str | None = None,
        show_value: bool = False,
        foreground_color: Literal[
            "primary",
            "secondary",
            "destructive",
            "muted",
            "accent",
            "popover",
            "card",
            "background",
            "foreground",
        ]
        | None = None,
        track_color: str | None = None,
        striped: str | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.value = value
        self.max = max
        self.label = label
        self.show_value = show_value
        self.foreground_color = foreground_color
        self.track_color = track_color
        self.striped = striped

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "value": self.value,
                "max": self.max,
                "label": self.label,
                "show_value": self.show_value,
                "foreground_color": self.foreground_color,
                "track_color": self.track_color,
                "striped": self.striped,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [],
        }


class Skeleton(Component):
    """Skeleton loading placeholder."""

    component_type: str = "Skeleton"

    def __init__(
        self,
        width: str | int | None = None,
        height: str | int | None = None,
        variant: Literal["text", "circular", "rectangular"] = "text",
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.width = width
        self.height = height
        self.variant = variant

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "width": self.width,
                "height": self.height,
                "variant": self.variant,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [],
        }


class ConnectionStatus(Component):
    """
    Component that conditionally shows content based on WebSocket connection state.

    Can trigger callbacks on connection state changes for both frontend (JS)
    and backend (Python) handling.

    Example:
        ```python
        ConnectionStatus(
            children_connected=[
                Badge("Online", variant="success")
            ],
            children_disconnected=[
                Alert(
                    title="Connection Lost",
                    message="Attempting to reconnect...",
                    variant="destructive"
                )
            ],
            position="bottom-right",
            on_disconnect=ctx.callback(handle_disconnect),
            on_reconnect=ctx.callback(handle_reconnect),
            js_on_disconnect=ctx.js("console.log('Disconnected!')"),
            js_on_reconnect=ctx.js("console.log('Reconnected!')"),
        )
        ```

    Args:
        children_connected: Content to show when connected (optional)
        children_disconnected: Content to show when disconnected (optional)
        position: Position on screen - 'top-left', 'top-right', 'bottom-left',
            'bottom-right', or 'inline'
        on_disconnect: Python callback to invoke when connection is lost
        on_reconnect: Python callback to invoke when connection is restored
        js_on_disconnect: JavaScript callback to execute when connection is lost
        js_on_reconnect: JavaScript callback to execute when connection is restored
        debounce_ms: Debounce time in ms before firing callbacks (default 500)
    """

    component_type: str = "ConnectionStatus"

    def __init__(
        self,
        children_connected: list[Component | str] | None = None,
        children_disconnected: list[Component | str] | None = None,
        position: Literal[
            "top-left", "top-right", "bottom-left", "bottom-right", "inline"
        ] = "bottom-right",
        on_disconnect: Any = None,
        on_reconnect: Any = None,
        js_on_disconnect: Any = None,
        js_on_reconnect: Any = None,
        debounce_ms: int = 500,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.children_connected = children_connected or []
        self.children_disconnected = children_disconnected or []
        self.position = position
        self.on_disconnect = on_disconnect
        self.on_reconnect = on_reconnect
        self.js_on_disconnect = js_on_disconnect
        self.js_on_reconnect = js_on_reconnect
        self.debounce_ms = debounce_ms

    def _render_child_list(self, children: list[Component | str]) -> list[dict[str, Any] | str]:
        """Render a list of children to dicts."""
        result = []
        for child in children:
            if isinstance(child, Component):
                result.append(child.render())
            else:
                result.append(str(child))
        return result

    def render(self) -> dict[str, Any]:
        props: dict[str, Any] = {
            "children_connected": self._render_child_list(self.children_connected),
            "children_disconnected": self._render_child_list(self.children_disconnected),
            "position": self.position,
            "debounce_ms": self.debounce_ms,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        # Serialize callbacks if present
        if self.on_disconnect:
            props["on_disconnect"] = self.on_disconnect.serialize()
        if self.on_reconnect:
            props["on_reconnect"] = self.on_reconnect.serialize()
        if self.js_on_disconnect:
            props["js_on_disconnect"] = self.js_on_disconnect.serialize()
        if self.js_on_reconnect:
            props["js_on_reconnect"] = self.js_on_reconnect.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": [],
        }
