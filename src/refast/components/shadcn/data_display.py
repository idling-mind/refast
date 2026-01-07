"""Data display components based on shadcn."""

from typing import Any, Literal

from refast.components.base import Component


class Table(Component):
    """
    Table container component.

    Example:
        ```python
        Table(
            children=[
                TableHeader(children=[
                    TableRow(children=[
                        TableHead(children=["Name"]),
                        TableHead(children=["Email"]),
                    ])
                ]),
                TableBody(children=[
                    TableRow(children=[
                        TableCell(children=["John"]),
                        TableCell(children=["john@example.com"]),
                    ])
                ])
            ]
        )
        ```
    """

    component_type: str = "Table"

    def __init__(
        self,
        children: list["Component | str"] | None = None,
        caption: str | None = None,
        striped: bool = False,
        hoverable: bool = False,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children
        self.caption = caption
        self.striped = striped
        self.hoverable = hoverable

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "caption": self.caption,
                "striped": self.striped,
                "hoverable": self.hoverable,
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class TableHeader(Component):
    """Table header section."""

    component_type: str = "TableHeader"

    def __init__(
        self,
        children: list["Component | str"] | None = None,
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
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class TableBody(Component):
    """Table body section."""

    component_type: str = "TableBody"

    def __init__(
        self,
        children: list["Component | str"] | None = None,
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
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class TableRow(Component):
    """Table row."""

    component_type: str = "TableRow"

    def __init__(
        self,
        children: list["Component | str"] | None = None,
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
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class TableHead(Component):
    """Table header cell."""

    component_type: str = "TableHead"

    def __init__(
        self,
        children: list["Component | str"] | None = None,
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
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class TableCell(Component):
    """Table data cell."""

    component_type: str = "TableCell"

    def __init__(
        self,
        children: list["Component | str"] | None = None,
        col_span: int | None = None,
        row_span: int | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children
        self.col_span = col_span
        self.row_span = row_span

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "colSpan": self.col_span,
                "rowSpan": self.row_span,
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class DataTable(Component):
    """Data table with sorting, filtering, and pagination."""

    component_type: str = "DataTable"

    def __init__(
        self,
        columns: list[dict[str, Any]],
        data: list[dict[str, Any]],
        sortable: bool = True,
        filterable: bool = True,
        paginated: bool = True,
        page_size: int = 10,
        on_row_click: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.columns = columns
        self.data = data
        self.sortable = sortable
        self.filterable = filterable
        self.paginated = paginated
        self.page_size = page_size
        self.on_row_click = on_row_click

    def render(self) -> dict[str, Any]:
        props = {
            "columns": self.columns,
            "data": self.data,
            "sortable": self.sortable,
            "filterable": self.filterable,
            "paginated": self.paginated,
            "pageSize": self.page_size,
            "className": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.on_row_click:
            props["onRowClick"] = self.on_row_click.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": [],
        }


class List(Component):
    """List component for displaying items."""

    component_type: str = "List"

    def __init__(
        self,
        children: list[Component | str] | None = None,
        ordered: bool = False,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children
        self.ordered = ordered

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "ordered": self.ordered,
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class Badge(Component):
    """Badge component for labels and tags."""

    component_type: str = "Badge"

    def __init__(
        self,
        children: list["Component | str"] | None = None,
        variant: Literal[
            "default", "primary", "secondary", "destructive", "outline", "success", "warning"
        ] = "default",
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children
        self.variant = variant

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "variant": self.variant,
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class Avatar(Component):
    """Avatar component for user images."""

    component_type: str = "Avatar"

    def __init__(
        self,
        src: str | None = None,
        alt: str = "",
        fallback: str | None = None,
        size: Literal["sm", "md", "lg", "xl"] = "md",
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.src = src
        self.alt = alt
        self.fallback = fallback
        self.size = size

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "src": self.src,
                "alt": self.alt,
                "fallback": self.fallback,
                "size": self.size,
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [],
        }


class Tooltip(Component):
    """Tooltip component for hover information."""

    component_type: str = "Tooltip"

    def __init__(
        self,
        content: str,
        children: list[Component | str] | None = None,
        side: Literal["top", "right", "bottom", "left"] = "top",
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children
        self.content = content
        self.side = side

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "content": self.content,
                "side": self.side,
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class Tabs(Component):
    """Tabs container component."""

    component_type: str = "Tabs"

    def __init__(
        self,
        children: list[Component | str] | None = None,
        default_value: str | None = None,
        value: str | None = None,
        on_value_change: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children
        self.default_value = default_value
        self.value = value
        self.on_value_change = on_value_change

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "defaultValue": self.default_value,
                "value": self.value,
                "onValueChange": (
                    self.on_value_change.serialize() if self.on_value_change else None
                ),
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class TabItem(Component):
    """Individual tab item."""

    component_type: str = "TabItem"

    def __init__(
        self,
        value: str,
        label: str,
        children: list[Component | str] | None = None,
        disabled: bool = False,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children
        self.value = value
        self.label = label
        self.disabled = disabled

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "value": self.value,
                "label": self.label,
                "disabled": self.disabled,
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class Accordion(Component):
    """
    Accordion container component.

    Example:
        ```python
        Accordion(
            type="single",
            collapsible=True,
            children=[
                AccordionItem(
                    value="item-1",
                    children=[
                        AccordionTrigger(children=["Is it accessible?"]),
                        AccordionContent(children=["Yes."])
                    ]
                )
            ]
        )
        ```
    """

    component_type: str = "Accordion"

    def __init__(
        self,
        children: list["Component | str"] | None = None,
        type: Literal["single", "multiple"] = "single",
        collapsible: bool = True,
        default_value: str | list[str] | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children
        self.accordion_type = type
        self.collapsible = collapsible
        self.default_value = default_value

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "type": self.accordion_type,
                "collapsible": self.collapsible,
                "defaultValue": self.default_value,
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class AccordionItem(Component):
    """Accordion item component."""

    component_type: str = "AccordionItem"

    def __init__(
        self,
        value: str,
        children: list["Component | str"] | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.value = value
        if children:
            self._children = children

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "value": self.value,
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class AccordionTrigger(Component):
    """Accordion trigger component."""

    component_type: str = "AccordionTrigger"

    def __init__(
        self,
        children: list["Component | str"] | None = None,
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
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class AccordionContent(Component):
    """Accordion content component."""

    component_type: str = "AccordionContent"

    def __init__(
        self,
        children: list["Component | str"] | None = None,
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
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }
