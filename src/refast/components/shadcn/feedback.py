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
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "title": self.title,
                "message": self.message,
                "variant": self.variant,
                "dismissible": self.dismissible,
                "onDismiss": self.on_dismiss.serialize() if self.on_dismiss else None,
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class Toast(Component):
    """Toast notification component (typically triggered programmatically)."""

    component_type: str = "Toast"

    def __init__(
        self,
        title: str | None = None,
        message: str | None = None,
        variant: Literal["default", "success", "warning", "destructive", "info"] = "default",
        duration: int = 3000,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.title = title
        self.message = message
        self.variant = variant
        self.duration = duration

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "title": self.title,
                "message": self.message,
                "variant": self.variant,
                "duration": self.duration,
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [],
        }


class Modal(Component):
    """Modal overlay component."""

    component_type: str = "Modal"

    def __init__(
        self,
        children: list[Component | str] | None = None,
        title: str | None = None,
        open: bool = False,
        on_close: Any = None,
        size: Literal["sm", "md", "lg", "xl", "full"] = "md",
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children
        self.title = title
        self.open = open
        self.on_close = on_close
        self.size = size

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "title": self.title,
                "open": self.open,
                "onClose": self.on_close.serialize() if self.on_close else None,
                "size": self.size,
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class Dialog(Component):
    """Dialog component with header, content, and actions."""

    component_type: str = "Dialog"

    def __init__(
        self,
        children: list[Component | str] | None = None,
        title: str | None = None,
        description: str | None = None,
        open: bool = False,
        on_open_change: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children
        self.title = title
        self.description = description
        self.open = open
        self.on_open_change = on_open_change

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "title": self.title,
                "description": self.description,
                "open": self.open,
                "onOpenChange": (self.on_open_change.serialize() if self.on_open_change else None),
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
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
                "className": self.class_name,
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
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.value = value
        self.max = max
        self.label = label
        self.show_value = show_value

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "value": self.value,
                "max": self.max,
                "label": self.label,
                "showValue": self.show_value,
                "className": self.class_name,
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
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [],
        }
