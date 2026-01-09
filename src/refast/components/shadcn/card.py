"""Card components."""

from typing import Any

from refast.components.base import Component


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
        children: list[Component | str] | None = None,
        title: str | None = None,
        description: str | None = None,
        on_click: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children
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
    """Card header section."""

    component_type: str = "CardHeader"

    def __init__(
        self,
        title: str | None = None,
        description: str | None = None,
        children: list[Component | str] | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children
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
    """Card content section."""

    component_type: str = "CardContent"

    def __init__(
        self,
        children: list[Component | str] | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children

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
    """Card footer section."""

    component_type: str = "CardFooter"

    def __init__(
        self,
        children: list[Component | str] | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children

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
    """Card title component."""

    component_type: str = "CardTitle"

    def __init__(
        self,
        text: str = "",
        children: list[Component | str] | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.text = text
        if children:
            self._children = children
        elif text:
            self._children = [text]

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
    """Card description component."""

    component_type: str = "CardDescription"

    def __init__(
        self,
        text: str = "",
        children: list[Component | str] | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.text = text
        if children:
            self._children = children
        elif text:
            self._children = [text]

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

