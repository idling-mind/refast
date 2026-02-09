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
                "class_name": self.class_name,
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
                "class_name": self.class_name,
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
                "class_name": self.class_name,
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
                "class_name": self.class_name,
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
                "class_name": self.class_name,
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
                "col_span": self.col_span,
                "row_span": self.row_span,
                "class_name": self.class_name,
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
            "page_size": self.page_size,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.on_row_click:
            props["on_row_click"] = self.on_row_click.serialize()

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
                "class_name": self.class_name,
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
                "class_name": self.class_name,
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
                "class_name": self.class_name,
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
        side_offset: int | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children
        self.content = content
        self.side = side
        self.side_offset = side_offset

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "content": self.content,
                "side": self.side,
                "side_offset": self.side_offset,
                "class_name": self.class_name,
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
                "default_value": self.default_value,
                "value": self.value,
                "on_value_change": (
                    self.on_value_change.serialize() if self.on_value_change else None
                ),
                "class_name": self.class_name,
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
                "class_name": self.class_name,
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
            on_value_change=ctx.callback(handle_change),
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

    Args:
        children: List of AccordionItem components.
        type: "single" allows one item open at a time, "multiple" allows multiple.
        collapsible: If True and type="single", allows closing all items.
        default_value: Initially open item(s). String for single, list for multiple.
        on_value_change: Callback when the open items change. Receives {"value": ...}.
    """

    component_type: str = "Accordion"

    def __init__(
        self,
        children: list["Component | str"] | None = None,
        type: Literal["single", "multiple"] = "single",
        collapsible: bool = True,
        default_value: str | list[str] | None = None,
        on_value_change: Any = None,
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
        self.on_value_change = on_value_change

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "type": self.accordion_type,
                "collapsible": self.collapsible,
                "default_value": self.default_value,
                "on_value_change": (
                    self.on_value_change.serialize() if self.on_value_change else None
                ),
                "class_name": self.class_name,
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
                "class_name": self.class_name,
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
                "class_name": self.class_name,
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
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class Image(Component):
    """
    Image component with loading state and fallback support.

    Example:
        ```python
        Image(
            src="/images/photo.jpg",
            alt="A beautiful photo",
            width=400,
            height=300,
            object_fit="cover",
            loading=True,
            fallback_src="/images/placeholder.jpg",
        )
        ```

    Args:
        src: The image source URL.
        alt: Alternative text for the image.
        width: Width of the image (number in pixels or CSS string).
        height: Height of the image (number in pixels or CSS string).
        object_fit: Object fit style - how the image should be resized to fit its container.
        loading: Whether to show a loading skeleton while the image loads.
        fallback_src: Fallback image URL to show if the main image fails to load.
    """

    component_type: str = "Image"

    def __init__(
        self,
        src: str,
        alt: str = "",
        width: int | str | None = None,
        height: int | str | None = None,
        object_fit: Literal["contain", "cover", "fill", "none", "scale-down"] = "cover",
        loading: bool = False,
        fallback_src: str | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.src = src
        self.alt = alt
        self.width = width
        self.height = height
        self.object_fit = object_fit
        self.loading = loading
        self.fallback_src = fallback_src

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "src": self.src,
                "alt": self.alt,
                "width": self.width,
                "height": self.height,
                "object_fit": self.object_fit,
                "loading": self.loading,
                "fallback_src": self.fallback_src,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [],
        }
