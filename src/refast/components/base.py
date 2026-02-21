"""Base component classes."""

import logging
import os
import re
import uuid
from abc import ABC, abstractmethod
from typing import Any, Self, Union

logger = logging.getLogger(__name__)

# Enable prop validation in development mode
_VALIDATE_PROPS = os.environ.get("REFAST_VALIDATE_PROPS", "").lower() in ("1", "true", "yes")

# Type alias for children
ChildrenType = Union[list[Union["Component", str, None]], "Component", str, None]


def _has_camel_case(key: str) -> bool:
    """Check if a key appears to be camelCase (has lowercase followed by uppercase)."""
    # Skip keys that are all lowercase or start with underscore
    if "_" in key or key.startswith("_"):
        return False
    return bool(re.search(r"[a-z][A-Z]", key))


def _validate_prop_keys(props: dict[str, Any], component_type: str) -> None:
    """
    Validate that prop keys use snake_case convention.

    In development mode (REFAST_VALIDATE_PROPS=1), this will log warnings
    for any camelCase keys found in props.
    """
    if not _VALIDATE_PROPS:
        return

    camel_keys = [key for key in props.keys() if _has_camel_case(key)]
    if camel_keys:
        logger.warning(
            f"[{component_type}] Props contain camelCase keys which should be snake_case: "
            f"{camel_keys}. The frontend will NOT convert these correctly. "
            f"Use snake_case (e.g., 'icon_position' instead of 'iconPosition')."
        )


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
        parent_style: dict[str, Any] | None = None,
        **props: Any,
    ):
        self.id = id or str(uuid.uuid4())
        self.class_name = class_name
        self.style = style or {}
        self.parent_style = parent_style or {}
        self.extra_props = props
        self._children: list[Component | str | None] = []

    def add_child(self, child: Union["Component", str, None]) -> Self:
        """Add a child component."""
        self._children.append(child)
        return self

    def add_children(self, children: ChildrenType) -> Self:
        """Add multiple children or a single child."""
        if children is None:
            return self

        if isinstance(children, list):
            self._children.extend(children)
        else:
            self._children.append(children)
        return self

    def _render_children(self) -> list[dict[str, Any] | str]:
        """Render all children to dicts, filtering out None values."""
        result = []
        for child in self._children:
            if child is None:
                continue
            if isinstance(child, Component):
                result.append(child.render())
            else:
                result.append(str(child))
        return result

    def _serialize_extra_props(self) -> dict[str, Any]:
        """Serialize extra_props, handling Callback objects."""
        result = {}
        for key, value in self.extra_props.items():
            if hasattr(value, "serialize") and callable(value.serialize):
                # Keep snake_case - frontend will convert to camelCase
                result[key] = value.serialize()
            else:
                result[key] = value

        if self.style:
            result["style"] = self.style
        if self.parent_style:
            result["parent_style"] = self.parent_style

        return result

    def _validate_props(self, props: dict[str, Any]) -> None:
        """
        Validate that props use snake_case convention.

        Call this in development to catch camelCase prop keys early.
        Enable validation by setting REFAST_VALIDATE_PROPS=1 environment variable.

        Args:
            props: The props dictionary to validate
        """
        _validate_prop_keys(props, self.component_type)

    @staticmethod
    def _to_camel_case(snake_str: str) -> str:
        """Convert snake_case to camelCase. Deprecated - frontend handles conversion."""
        components = snake_str.split("_")
        return components[0] + "".join(x.title() for x in components[1:])

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
        children: ChildrenType = None,
        id: str | None = None,
        class_name: str = "",
        style: dict[str, Any] | None = None,
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, style=style, **props)
        self.add_children(children)

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "class_name": self.class_name,
                "style": self.style,
                **self._serialize_extra_props(),
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
                "class_name": self.class_name,
                "style": self.style,
                **self._serialize_extra_props(),
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

    def __init__(self, children: ChildrenType = None):
        super().__init__()
        self.add_children(children)

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {},
            "children": self._render_children(),
        }
