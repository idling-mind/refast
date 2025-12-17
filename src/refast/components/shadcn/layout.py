"""Layout components based on shadcn."""

from typing import Any, Literal

from refast.components.base import Component


class Row(Component):
    """
    Horizontal flex container.

    Example:
        ```python
        Row(
            children=[Button("A"), Button("B")],
            justify="between",
            align="center",
            gap=4,
        )
        ```
    """

    component_type: str = "Row"

    def __init__(
        self,
        children: list[Component | str] | None = None,
        justify: Literal["start", "end", "center", "between", "around", "evenly"] = "start",
        align: Literal["start", "end", "center", "stretch", "baseline"] = "start",
        gap: int | str = 0,
        wrap: bool = False,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children
        self.justify = justify
        self.align = align
        self.gap = gap
        self.wrap = wrap

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "justify": self.justify,
                "align": self.align,
                "gap": self.gap,
                "wrap": self.wrap,
                "className": self.class_name,
                **self.extra_props,
            },
            "children": self._render_children(),
        }


class Column(Component):
    """
    Vertical flex container.

    Example:
        ```python
        Column(
            children=[Text("Line 1"), Text("Line 2")],
            gap=2,
        )
        ```
    """

    component_type: str = "Column"

    def __init__(
        self,
        children: list[Component | str] | None = None,
        justify: Literal["start", "end", "center", "between", "around", "evenly"] = "start",
        align: Literal["start", "end", "center", "stretch", "baseline"] = "stretch",
        gap: int | str = 0,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children
        self.justify = justify
        self.align = align
        self.gap = gap

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "justify": self.justify,
                "align": self.align,
                "gap": self.gap,
                "className": self.class_name,
                **self.extra_props,
            },
            "children": self._render_children(),
        }


class Stack(Component):
    """
    Stack container with consistent spacing.

    Similar to Column but with simpler API for common use cases.
    """

    component_type: str = "Stack"

    def __init__(
        self,
        children: list[Component | str] | None = None,
        spacing: int | str = 4,
        direction: Literal["vertical", "horizontal"] = "vertical",
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children
        self.spacing = spacing
        self.direction = direction

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "spacing": self.spacing,
                "direction": self.direction,
                "className": self.class_name,
                **self.extra_props,
            },
            "children": self._render_children(),
        }


class Grid(Component):
    """
    CSS Grid container.

    Example:
        ```python
        Grid(
            children=[Card(...) for _ in range(6)],
            columns=3,
            gap=4,
        )
        ```
    """

    component_type: str = "Grid"

    def __init__(
        self,
        children: list[Component | str] | None = None,
        columns: int | str = 1,
        rows: int | str | None = None,
        gap: int | str = 0,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children
        self.columns = columns
        self.rows = rows
        self.gap = gap

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "columns": self.columns,
                "rows": self.rows,
                "gap": self.gap,
                "className": self.class_name,
                **self.extra_props,
            },
            "children": self._render_children(),
        }


class Flex(Component):
    """Generic flexbox container with full control."""

    component_type: str = "Flex"

    def __init__(
        self,
        children: list[Component | str] | None = None,
        direction: Literal["row", "column", "row-reverse", "column-reverse"] = "row",
        justify: str = "start",
        align: str = "stretch",
        wrap: Literal["nowrap", "wrap", "wrap-reverse"] = "nowrap",
        gap: int | str = 0,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children
        self.direction = direction
        self.justify = justify
        self.align = align
        self.wrap = wrap
        self.gap = gap

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "direction": self.direction,
                "justify": self.justify,
                "align": self.align,
                "wrap": self.wrap,
                "gap": self.gap,
                "className": self.class_name,
                **self.extra_props,
            },
            "children": self._render_children(),
        }


class Center(Component):
    """Center content horizontally and vertically."""

    component_type: str = "Center"

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
                "className": self.class_name,
                **self.extra_props,
            },
            "children": self._render_children(),
        }


class Spacer(Component):
    """Flexible spacer that expands to fill available space."""

    component_type: str = "Spacer"

    def __init__(self, size: int | str | None = None, **props: Any):
        super().__init__(**props)
        self.size = size

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {"size": self.size, **self.extra_props},
            "children": [],
        }


class Divider(Component):
    """Horizontal or vertical divider line."""

    component_type: str = "Divider"

    def __init__(
        self,
        orientation: Literal["horizontal", "vertical"] = "horizontal",
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.orientation = orientation

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "orientation": self.orientation,
                "className": self.class_name,
                **self.extra_props,
            },
            "children": [],
        }
