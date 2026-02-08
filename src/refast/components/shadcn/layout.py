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
        gap: int | str = 2,
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
                "class_name": self.class_name,
                **self._serialize_extra_props(),
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
        gap: int | str = 2,
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
                "class_name": self.class_name,
                **self._serialize_extra_props(),
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
        gap: int | str = 4,
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
                "class_name": self.class_name,
                **self._serialize_extra_props(),
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
        gap: int | str = 2,
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
                "class_name": self.class_name,
                **self._serialize_extra_props(),
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
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }

