"""Base component classes."""

import uuid
from abc import ABC, abstractmethod
from typing import Any, Self


class Component(ABC):
    """
    Base class for all Refast components.

    Components are Python objects that render to a dictionary structure
    that the frontend can interpret and render as React components.

    Example:
        ```python
        class MyButton(Component):
            component_type = "Button"

            def __init__(self, label: str, on_click: Callback | None = None):
                super().__init__()
                self.label = label
                self.on_click = on_click

            def render(self) -> dict[str, Any]:
                return {
                    "type": self.component_type,
                    "id": self.id,
                    "props": {"label": self.label},
                    "children": [],
                }
        ```
    """

    component_type: str = "Component"

    def __init__(
        self,
        id: str | None = None,
        class_name: str = "",
        style: dict[str, Any] | None = None,
        **props: Any,
    ):
        self.id = id or str(uuid.uuid4())
        self.class_name = class_name
        self.style = style or {}
        self.extra_props = props
        self._children: list[Component | str] = []

    def add_child(self, child: "Component | str") -> Self:
        """Add a child component."""
        self._children.append(child)
        return self

    def add_children(self, children: list["Component | str"]) -> Self:
        """Add multiple children."""
        self._children.extend(children)
        return self

    def _render_children(self) -> list[dict[str, Any] | str]:
        """Render all children to dicts."""
        result = []
        for child in self._children:
            if isinstance(child, Component):
                result.append(child.render())
            else:
                result.append(str(child))
        return result

    @abstractmethod
    def render(self) -> dict[str, Any]:
        """
        Render the component to a dictionary.

        Returns:
            Dictionary with type, id, props, and children
        """
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r})"


class Container(Component):
    """
    Generic container component.

    Example:
        ```python
        Container(
            id="main",
            class_name="p-4",
            children=[
                Text("Hello"),
                Button("Click me"),
            ]
        )
        ```
    """

    component_type: str = "Container"

    def __init__(
        self,
        children: list["Component | str"] | None = None,
        id: str | None = None,
        class_name: str = "",
        style: dict[str, Any] | None = None,
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, style=style, **props)
        if children:
            self._children = children

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "className": self.class_name,
                "style": self.style,
                **self.extra_props,
            },
            "children": self._render_children(),
        }


class Text(Component):
    """
    Text component for displaying text content.

    Example:
        ```python
        Text("Hello, World!", class_name="text-lg font-bold")
        ```
    """

    component_type: str = "Text"

    def __init__(
        self,
        content: str,
        id: str | None = None,
        class_name: str = "",
        style: dict[str, Any] | None = None,
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, style=style, **props)
        self.content = content

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "className": self.class_name,
                "style": self.style,
                **self.extra_props,
            },
            "children": [self.content],
        }


class Fragment(Component):
    """
    Fragment component for grouping without a wrapper element.

    Example:
        ```python
        Fragment([
            Text("Line 1"),
            Text("Line 2"),
        ])
        ```
    """

    component_type: str = "Fragment"

    def __init__(self, children: list["Component | str"] | None = None):
        super().__init__()
        if children:
            self._children = children

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {},
            "children": self._render_children(),
        }
