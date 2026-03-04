"""Card components."""

from typing import Any

from refast.components.base import ChildrenType, Component


class Card(Component):
    """
    Card container component.

    Example:
        ```python
        Card(
            children=[
                CardHeader(title="My Card"),
                CardContent(children=[Text("Content here")]),
                CardFooter(children=[Button("Action")]),
            ]
        )
        ```
    """

    component_type: str = "Card"

    def __init__(
        self,
        children: ChildrenType = None,
        title: str | None = None,
        description: str | None = None,
        on_click: Any = None,
        id: str | None = None,
        class_name: str = "",
        style: dict[str, Any] | None = None,
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, style=style, **props)
        self.add_children(children)
        self.title = title
        self.description = description
        self.on_click = on_click

    def render(self) -> dict[str, Any]:
        props = {
            "title": self.title,
            "description": self.description,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.on_click:
            props["on_click"] = self.on_click.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": self._render_children(),
        }


class CardHeader(Component):
    """
    Card header section.

    Renders as a vertically-stacked flex container at the top of the card.
    Typically wraps :class:`CardTitle` and :class:`CardDescription`, or accepts
    a ``title``/``description`` shorthand that the React component renders
    directly.

    Example:
        ```python
        CardHeader(title="Dashboard", description="Overview of your metrics")

        # Or with explicit sub-components:
        CardHeader(children=[
            CardTitle("Dashboard"),
            CardDescription("Overview of your metrics"),
        ])
        ```

    Args:
        title: Shorthand title text rendered as a heading inside the header.
        description: Shorthand subtitle text rendered below the title.
        children: Explicit child components (used instead of ``title``/
            ``description`` when fine-grained control is needed).
        id: Optional HTML element id.
        class_name: Additional CSS class names.
        style: Inline CSS style dict.
    """

    component_type: str = "CardHeader"

    def __init__(
        self,
        title: str | None = None,
        description: str | None = None,
        children: ChildrenType = None,
        id: str | None = None,
        class_name: str = "",
        style: dict[str, Any] | None = None,
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, style=style, **props)
        self.add_children(children)
        self.title = title
        self.description = description

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "title": self.title,
                "description": self.description,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class CardContent(Component):
    """
    Card body content section.

    Rendered with appropriate padding below any :class:`CardHeader`. This is
    the primary area for the card's main content.

    Example:
        ```python
        CardContent(children=[Text("Main content goes here.")])
        ```

    Args:
        children: Content to display in the card body.
        id: Optional HTML element id.
        class_name: Additional CSS class names.
        style: Inline CSS style dict.
    """

    component_type: str = "CardContent"

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
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class CardFooter(Component):
    """
    Card footer section.

    Rendered as an inline flex row at the bottom of the card. Typically used
    for action buttons.

    Example:
        ```python
        CardFooter(children=[
            Button("Cancel", variant="outline"),
            Button("Save", on_click=ctx.callback(save)),
        ])
        ```

    Args:
        children: Footer content — typically action buttons.
        id: Optional HTML element id.
        class_name: Additional CSS class names.
        style: Inline CSS style dict.
    """

    component_type: str = "CardFooter"

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
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class CardTitle(Component):
    """
    Card title text.

    Renders as a prominent ``<h3>`` heading inside the card. Pass the title
    text as ``children``.

    Example:
        ```python
        CardTitle("Dashboard")
        CardTitle(children=["Dashboard"])
        ```

    Args:
        children: Title text or components.
        id: Optional HTML element id.
        class_name: Additional CSS class names.
        style: Inline CSS style dict.
    """

    component_type: str = "CardTitle"

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
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class CardDescription(Component):
    """
    Card description / subtitle text.

    Renders as a muted ``<p>`` tag beneath the title. Pass the description
    text as ``children``.

    Example:
        ```python
        CardDescription("Overview of your metrics")
        CardDescription(children=["Overview of your metrics"])
        ```

    Args:
        children: Description text or components.
        id: Optional HTML element id.
        class_name: Additional CSS class names.
        style: Inline CSS style dict.
    """

    component_type: str = "CardDescription"

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
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }
