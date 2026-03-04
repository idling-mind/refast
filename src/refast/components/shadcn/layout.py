"""Layout components based on shadcn."""

from typing import Any, Literal

from refast.components.base import ChildrenType, Component


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

    Args:
        children: Child components to render inside the row.
        justify: Justify-content value. One of ``"start"``, ``"end"``,
            ``"center"``, ``"between"``, ``"around"``, or ``"evenly"``.
        align: Align-items value. One of ``"start"``, ``"end"``,
            ``"center"``, ``"stretch"``, or ``"baseline"``.
        gap: Gap between children as a Tailwind spacing integer (multiplied
            by 0.25 rem on the React side). Defaults to ``2``.
        wrap: Whether children wrap onto multiple lines. Defaults to ``False``.
        id: Optional unique element ID for targeted updates.
        class_name: Additional Tailwind CSS classes.
    """

    component_type: str = "Row"

    def __init__(
        self,
        children: ChildrenType = None,
        justify: Literal["start", "end", "center", "between", "around", "evenly"] = "start",
        align: Literal["start", "end", "center", "stretch", "baseline"] = "start",
        gap: int = 2,
        wrap: bool = False,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.add_children(children)
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

    Args:
        children: Child components to render inside the column.
        justify: Justify-content value. One of ``"start"``, ``"end"``,
            ``"center"``, ``"between"``, ``"around"``, or ``"evenly"``.
        align: Align-items value. One of ``"start"``, ``"end"``,
            ``"center"``, ``"stretch"``, or ``"baseline"``.
        gap: Gap between children as a Tailwind spacing integer. Defaults to ``2``.
        wrap: Whether children wrap onto multiple lines. Defaults to ``False``.
        id: Optional unique element ID for targeted updates.
        class_name: Additional Tailwind CSS classes.
    """

    component_type: str = "Column"

    def __init__(
        self,
        children: ChildrenType = None,
        justify: Literal["start", "end", "center", "between", "around", "evenly"] = "start",
        align: Literal["start", "end", "center", "stretch", "baseline"] = "stretch",
        gap: int = 2,
        wrap: bool = False,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.add_children(children)
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

    Args:
        children: Child components rendered as grid cells.
        columns: Number of equal-width columns, or a custom
            ``gridTemplateColumns`` string. Defaults to ``1``.
        rows: Number of equal-height rows, or a custom ``gridTemplateRows``
            string. ``None`` lets the browser decide. Defaults to ``None``.
        gap: Gap between cells as a Tailwind spacing integer. Defaults to ``4``.
        id: Optional unique element ID for targeted updates.
        class_name: Additional Tailwind CSS classes.
    """

    component_type: str = "Grid"

    def __init__(
        self,
        children: ChildrenType = None,
        columns: int | str = 1,
        rows: int | str | None = None,
        gap: int = 4,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.add_children(children)
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
    """
    Generic flexbox container with full directional control.

    Under the hood this delegates to ``Row`` (``direction="row"``) or
    ``Column`` (``direction="column"``) on the React side.  For most
    use-cases prefer :class:`Row` or :class:`Column` directly.

    Example:
        ```python
        Flex(
            direction="row",
            justify="between",
            align="center",
            gap=4,
            wrap=True,
            children=[...],
        )
        ```

    Args:
        children: Child components to render.
        direction: Flex direction — ``"row"``, ``"column"``,
            ``"row-reverse"``, or ``"column-reverse"``.
        justify: Justify-content value. One of ``"start"``, ``"end"``,
            ``"center"``, ``"between"``, ``"around"``, or ``"evenly"``.
        align: Align-items value. One of ``"start"``, ``"end"``,
            ``"center"``, ``"stretch"``, or ``"baseline"``.
        wrap: Whether children wrap onto multiple lines. Defaults to ``False``.
        gap: Gap between children as a Tailwind spacing integer. Defaults to ``2``.
        id: Optional unique element ID for targeted updates.
        class_name: Additional Tailwind CSS classes.
    """

    component_type: str = "Flex"

    def __init__(
        self,
        children: ChildrenType = None,
        direction: Literal["row", "column", "row-reverse", "column-reverse"] = "row",
        justify: Literal["start", "end", "center", "between", "around", "evenly"] = "start",
        align: Literal["start", "end", "center", "stretch", "baseline"] = "stretch",
        wrap: bool = False,
        gap: int = 2,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.add_children(children)
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
    """
    Centers its children both horizontally and vertically.

    Renders a ``<div class="flex items-center justify-center">``.

    Example:
        ```python
        Center(
            children=[Heading("Welcome", level=1)],
            class_name="h-screen",
        )
        ```

    Args:
        children: Child components to center.
        id: Optional unique element ID for targeted updates.
        class_name: Additional Tailwind CSS classes.
    """

    component_type: str = "Center"

    def __init__(
        self,
        children: ChildrenType = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
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
