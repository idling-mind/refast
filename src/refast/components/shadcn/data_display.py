"""Data display components based on shadcn."""

from typing import Any, Literal

from refast.components.base import ChildrenType, Component


class Table(Component):
    """
    Table container component.

    Use the primitive ``Table*`` family when you need full layout control —
    custom cell rendering, row selection, or complex filters. For a turnkey
    solution with sorting, filtering, and pagination see :class:`DataTable`.

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

    Args:
        children: ``TableHeader`` and ``TableBody`` components.
        id: Optional HTML element id.
        class_name: Additional CSS class names.
    """

    component_type: str = "Table"

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


class TableHeader(Component):
    """
    Table header section (``<thead>``).

    Wraps one or more :class:`TableRow` components that contain
    :class:`TableHead` (``<th>``) cells.

    Example:
        ```python
        TableHeader(children=[
            TableRow(children=[
                TableHead(children=["Name"]),
                TableHead(children=["Email"]),
            ])
        ])
        ```

    Args:
        children: :class:`TableRow` components for the header.
        id: Optional HTML element id.
        class_name: Additional CSS class names.
    """

    component_type: str = "TableHeader"

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


class TableBody(Component):
    """
    Table body section (``<tbody>``).

    Wraps :class:`TableRow` components that form the data rows of the table.

    Example:
        ```python
        TableBody(children=[
            TableRow(children=[
                TableCell(children=["Alice"]),
                TableCell(children=["alice@example.com"]),
            ]),
            TableRow(children=[
                TableCell(children=["Bob"]),
                TableCell(children=["bob@example.com"]),
            ]),
        ])
        ```

    Args:
        children: :class:`TableRow` components for the body.
        id: Optional HTML element id.
        class_name: Additional CSS class names.
    """

    component_type: str = "TableBody"

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


class TableRow(Component):
    """
    Table row (``<tr>``).

    Used inside both :class:`TableHeader` and :class:`TableBody`. Each child
    should be a :class:`TableHead` (for header rows) or :class:`TableCell`
    (for body rows).

    Example:
        ```python
        TableRow(children=[
            TableCell(children=["Alice"]),
            TableCell(children=["alice@example.com"]),
        ])
        ```

    Args:
        children: :class:`TableHead` or :class:`TableCell` components.
        id: Optional HTML element id.
        class_name: Additional CSS class names.
    """

    component_type: str = "TableRow"

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


class TableHead(Component):
    """
    Table header cell (``<th>``).

    Used inside a :class:`TableRow` within a :class:`TableHeader`. The
    ``children`` are rendered as the column header label.

    Example:
        ```python
        TableHead(children=["Full Name"])
        TableHead(children=["Email"], class_name="text-right")
        ```

    Args:
        children: Cell content — typically a plain string label.
        id: Optional HTML element id.
        class_name: Additional CSS class names.
    """

    component_type: str = "TableHead"

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


class TableCell(Component):
    """
    Table data cell (``<td>``).

    Used inside a :class:`TableRow` within a :class:`TableBody`. Supports
    ``col_span`` and ``row_span`` for spanning multiple columns or rows.

    Example:
        ```python
        TableCell(children=["alice@example.com"])
        TableCell(children=["Total"], col_span=3, class_name="font-bold")
        ```

    Args:
        children: Cell content.
        col_span: Number of columns this cell should span.
        row_span: Number of rows this cell should span.
        id: Optional HTML element id.
        class_name: Additional CSS class names.
    """

    component_type: str = "TableCell"

    def __init__(
        self,
        children: ChildrenType = None,
        col_span: int | None = None,
        row_span: int | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.add_children(children)
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
    """
    High-level data table with built-in sorting, filtering, and pagination.

    Renders a complete table from column definitions and row data, handling all
    UI concerns (sort indicators, filter input, pagination controls) internally.
    For full layout control — custom cell rendering, row selection, or complex
    filters — use the lower-level :class:`Table`, :class:`TableHeader`,
    :class:`TableBody`, :class:`TableRow`, :class:`TableHead`, and
    :class:`TableCell` components instead.

    **Column definition format:**

    Each entry in ``columns`` is a ``dict`` with the following keys:

    +---------------+--------+----------+--------------------------------------------------+
    | Key           | Type   | Required | Description                                      |
    +===============+========+==========+==================================================+
    | ``key``       | str    | ✓        | Field name used to look up values in each row.   |
    +---------------+--------+----------+--------------------------------------------------+
    | ``header``    | str    | ✓        | Column header label.                             |
    +---------------+--------+----------+--------------------------------------------------+
    | ``sortable``  | bool   |          | Per-column sortable override. Falls back to the  |
    |               |        |          | component-level ``sortable`` flag if omitted.    |
    +---------------+--------+----------+--------------------------------------------------+
    | ``width``     | str    |          | CSS width (e.g. ``"200px"``, ``"20%"``).         |
    +---------------+--------+----------+--------------------------------------------------+
    | ``align``     | str    |          | ``"left"`` (default), ``"center"``, ``"right"``. |
    +---------------+--------+----------+--------------------------------------------------+

    Example:
        ```python
        from refast import Context, RefastApp
        from refast.components import Container, DataTable

        ui = RefastApp(title="Users")


        async def on_row_click(ctx: Context):
            row = ctx.event_data          # full row dict
            await ctx.show_toast(f"Clicked: {row['name']}")


        async def on_sort(ctx: Context):
            # event_data: {"key": "name", "direction": "asc"} or None
            ctx.state.set("sort", ctx.event_data)
            await ctx.refresh()


        async def on_page(ctx: Context):
            # event_data: {"page": 2}
            ctx.state.set("page", ctx.event_data.get("page", 1))
            await ctx.refresh()


        @ui.page("/")
        def home(ctx: Context):
            return Container(
                children=[
                    DataTable(
                        columns=[
                            {"key": "id",     "header": "#", "width": "60px", "align": "right"},
                            {"key": "name",   "header": "Name",   "sortable": True},
                            {"key": "email",  "header": "Email",  "sortable": True},
                            {"key": "role",   "header": "Role",   "align": "center"},
                            {"key": "status", "header": "Status", "sortable": True},
                        ],
                        data=[
                            {
                                "id": 1, "name": "Alice",
                                "email": "alice@example.com",
                                "role": "Admin", "status": "active",
                            },
                            {
                                "id": 2, "name": "Bob",
                                "email": "bob@example.com",
                                "role": "Editor", "status": "inactive",
                            },
                            {
                                "id": 3, "name": "Carol",
                                "email": "carol@example.com",
                                "role": "Viewer", "status": "pending",
                            },
                        ],
                        sortable=True,
                        filterable=True,
                        paginated=True,
                        page_size=10,
                        on_row_click=ctx.callback(on_row_click),
                        on_sort_change=ctx.callback(on_sort),
                        on_page_change=ctx.callback(on_page),
                        empty_message="No users found.",
                    )
                ]
            )
        ```

    Args:
        columns: List of column definition dicts. Each dict must contain ``key``
            (data field name) and ``header`` (display text). Optional keys:
            ``sortable`` (bool), ``width`` (CSS string), and ``align``
            (``"left"`` | ``"center"`` | ``"right"``).
        data: List of row dicts. Each dict should contain at least all keys
            referenced by ``columns``.
        sortable: Enable clicking column headers to sort. Individual columns can
            override this via their own ``sortable`` key. Defaults to ``True``.
        filterable: Show a text filter input above the table. Filters across
            all column values client-side. Defaults to ``True``.
        paginated: Show pagination controls below the table. Defaults to ``True``.
        page_size: Number of rows per page when ``paginated=True``. Defaults to ``10``.
        loading: Display a loading overlay on top of the table while data is
            being fetched. Defaults to ``False``.
        empty_message: Text shown when ``data`` is empty or no rows match the
            active filter. Defaults to ``"No data available"``.
        current_page: Controlled current page (1-based). When set, the component
            uses this value instead of managing page state internally. Pair with
            ``on_page_change`` for server-side pagination.
        on_row_click: Callback fired when a row is clicked. ``ctx.event_data``
            contains all key-value pairs of the clicked row.
        on_sort_change: Callback fired when sort state changes. ``ctx.event_data``
            is ``{"key": "<column_key>", "direction": "asc"|"desc"}`` or ``None``
            when sorting is cleared.
        on_filter_change: Callback fired when the filter input changes.
            ``ctx.event_data`` is ``{"value": "<filter_string>"}``.
        on_page_change: Callback fired when the active page changes.
            ``ctx.event_data`` is ``{"page": <page_number>}``.
        id: Optional HTML element id.
        class_name: Additional CSS class names.
    """

    component_type: str = "DataTable"

    def __init__(
        self,
        columns: list[dict[str, Any]],
        data: list[dict[str, Any]],
        sortable: bool = True,
        filterable: bool = True,
        paginated: bool = True,
        page_size: int = 10,
        loading: bool = False,
        empty_message: str = "No data available",
        current_page: int | None = None,
        on_row_click: Any = None,
        on_sort_change: Any = None,
        on_filter_change: Any = None,
        on_page_change: Any = None,
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
        self.loading = loading
        self.empty_message = empty_message
        self.current_page = current_page
        self.on_row_click = on_row_click
        self.on_sort_change = on_sort_change
        self.on_filter_change = on_filter_change
        self.on_page_change = on_page_change

    def render(self) -> dict[str, Any]:
        props: dict[str, Any] = {
            "columns": self.columns,
            "data": self.data,
            "sortable": self.sortable,
            "filterable": self.filterable,
            "paginated": self.paginated,
            "page_size": self.page_size,
            "loading": self.loading,
            "empty_message": self.empty_message,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.current_page is not None:
            props["current_page"] = self.current_page
        if self.on_row_click:
            props["on_row_click"] = self.on_row_click.serialize()
        if self.on_sort_change:
            props["on_sort_change"] = self.on_sort_change.serialize()
        if self.on_filter_change:
            props["on_filter_change"] = self.on_filter_change.serialize()
        if self.on_page_change:
            props["on_page_change"] = self.on_page_change.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": [],
        }


class List(Component):
    """
    Ordered or unordered list.

    Renders as ``<ol>`` or ``<ul>`` depending on the ``ordered`` flag.
    Children should be plain strings or ``ListItem`` components.

    Example:
        ```python
        List(children=["Apples", "Bananas", "Cherries"])
        List(ordered=True, children=["First step", "Second step", "Third step"])
        ```

    Args:
        children: List items — strings or ``ListItem`` components.
        ordered: If ``True``, renders a numbered ``<ol>``; otherwise a
            bulleted ``<ul>``. Defaults to ``False``.
        id: Optional HTML element id.
        class_name: Additional CSS class names.
    """

    component_type: str = "List"

    def __init__(
        self,
        children: ChildrenType = None,
        ordered: bool = False,
        id: str | None = None,
        class_name: str = "",
        style: dict[str, Any] | None = None,
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.add_children(children)
        self.ordered = ordered
        self.style = style

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "ordered": self.ordered,
                "class_name": self.class_name,
                "style": self.style,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class ListItem(Component):
    """
    List item component for use inside :class:`List`.

    Example:
        ```python
        List(children=[
            ListItem(children=["First item"]),
            ListItem(children=["Second item"]),
        ])
        ```

    Args:
        children: Item content — strings or nested components.
        id: Optional HTML element id.
        class_name: Additional CSS class names.
        style: Optional inline styles as a dictionary.
    """

    component_type: str = "ListItem"

    def __init__(
        self,
        children: ChildrenType = None,
        id: str | None = None,
        class_name: str = "",
        style: dict[str, Any] | None = None,
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.add_children(children)
        self.style = style

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


class Badge(Component):
    """
    Badge / tag component for labels, statuses, and counts.

    Example:
        ```python
        Badge(children=["New"])
        Badge(children=["Error"], variant="destructive")
        Badge(children=["Active"], variant="success")
        ```

    Args:
        children: Badge content — typically a short string.
        variant: Visual style. ``"default"`` is the primary filled style.
        id: Optional HTML element id.
        class_name: Additional CSS class names.
    """

    component_type: str = "Badge"

    def __init__(
        self,
        children: ChildrenType = None,
        variant: Literal[
            "default", "secondary", "destructive", "outline", "success", "warning"
        ] = "default",
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.add_children(children)
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
    """
    User avatar with image and initials fallback.

    Displays a circular user image. When the image is absent or fails to load,
    the ``fallback`` string (or the first character of ``alt``) is shown instead.

    Example:
        ```python
        # Image avatar
        Avatar(src="/avatars/alice.jpg", alt="Alice")

        # Initials-only avatar
        Avatar(fallback="JD", size="lg")
        ```

    Args:
        src: URL of the user image. Omit to show initials only.
        alt: Alternative text; also used to derive the fallback initial when
            ``fallback`` is not supplied.
        fallback: Short string (one or two letters) shown when the image is
            unavailable. Defaults to the first character of ``alt``.
        size: Avatar diameter. ``"sm"`` = 32 px, ``"md"`` = 40 px,
            ``"lg"`` = 48 px. Defaults to ``"md"``.
        id: Optional HTML element id.
        class_name: Additional CSS class names.
    """

    component_type: str = "Avatar"

    def __init__(
        self,
        src: str | None = None,
        alt: str = "",
        fallback: str | None = None,
        size: Literal["sm", "md", "lg"] = "md",
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
    """
    Hover tooltip that wraps any trigger element.

    The ``content`` string is shown in a floating popover when the user hovers
    over the child element. Exactly one child is expected as the trigger.

    Example:
        ```python
        Tooltip(
            content="This action cannot be undone.",
            children=[Button("Delete", variant="destructive")],
        )

        Tooltip(
            content="Home page",
            side="right",
            children=[IconButton(icon="home")],
        )
        ```

    Args:
        content: Plain-text tooltip message.
        children: The trigger element(s). Typically a single component.
        side: Preferred side of the trigger to display the tooltip.
            Defaults to ``"top"``.
        side_offset: Pixel gap between the trigger and the tooltip.
            Defaults to ``4``.
        id: Optional HTML element id applied to the trigger.
        class_name: Additional CSS class names applied to the tooltip content.
    """

    component_type: str = "Tooltip"

    def __init__(
        self,
        content: str,
        children: ChildrenType = None,
        side: Literal["top", "right", "bottom", "left"] = "top",
        side_offset: int | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.add_children(children)
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
    """
    Tab container that switches between :class:`TabItem` panels.

    Each direct child should be a :class:`TabItem`. The active panel is
    determined by the ``value`` / ``default_value`` props.

    Example:
        ```python
        Tabs(
            default_value="overview",
            children=[
                TabItem(value="overview", label="Overview",
                        children=[Text("Overview content")]),
                TabItem(value="settings", label="Settings",
                        children=[Text("Settings content")]),
            ],
        )
        ```

    Args:
        children: :class:`TabItem` components.
        default_value: Value of the initially active tab (uncontrolled).
        value: Controlled active tab value. Pair with ``on_value_change``.
        on_value_change: Callback fired when the active tab changes.
            ``ctx.event_data`` is the new tab value string.
        id: Optional HTML element id.
        class_name: Additional CSS class names.
    """

    component_type: str = "Tabs"

    def __init__(
        self,
        children: ChildrenType = None,
        default_value: str | None = None,
        value: str | None = None,
        on_value_change: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.add_children(children)
        self.default_value = default_value
        self.value = value
        self.on_value_change = on_value_change

    def render(self) -> dict[str, Any]:
        props: dict[str, Any] = {
            "default_value": self.default_value,
            "value": self.value,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }
        if self.on_value_change:
            props["on_value_change"] = self.on_value_change.serialize()
        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": self._render_children(),
        }


class TabItem(Component):
    """
    Individual tab panel inside a :class:`Tabs` container.

    ``value`` must be unique among siblings and is used to identify which panel
    is active. ``label`` is the human-readable text shown on the tab button.

    Example:
        ```python
        TabItem(
            value="settings",
            label="Settings",
            children=[Text("Manage your preferences here.")],
        )
        ```

    Args:
        value: Unique identifier for this panel within the :class:`Tabs` group.
        label: Text displayed on the tab trigger button.
        children: Panel content shown when this tab is active.
        disabled: If ``True``, the tab button is grayed out and non-clickable.
        id: Optional HTML element id.
        class_name: Additional CSS class names.
    """

    component_type: str = "TabItem"

    def __init__(
        self,
        value: str,
        label: str,
        children: ChildrenType = None,
        disabled: bool = False,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.add_children(children)
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
        value: Controlled open item(s). Pair with ``on_value_change`` for
            server-driven state. String for ``type="single"``, list for
            ``type="multiple"``.
        on_value_change: Callback when the open items change. Receives {"value": ...}.
    """

    component_type: str = "Accordion"

    def __init__(
        self,
        children: ChildrenType = None,
        type: Literal["single", "multiple"] = "single",
        collapsible: bool = True,
        default_value: str | list[str] | None = None,
        value: str | list[str] | None = None,
        on_value_change: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.add_children(children)
        self.accordion_type = type
        self.collapsible = collapsible
        self.default_value = default_value
        self.value = value
        self.on_value_change = on_value_change

    def render(self) -> dict[str, Any]:
        props: dict[str, Any] = {
            "type": self.accordion_type,
            "collapsible": self.collapsible,
            "default_value": self.default_value,
            "value": self.value,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }
        if self.on_value_change:
            props["on_value_change"] = self.on_value_change.serialize()
        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": self._render_children(),
        }


class AccordionItem(Component):
    """
    Individual collapsible section inside an :class:`Accordion`.

    Each ``AccordionItem`` contains one :class:`AccordionTrigger` (the
    clickable header) and one :class:`AccordionContent` (the revealed body).

    Example:
        ```python
        AccordionItem(
            value="faq-1",
            children=[
                AccordionTrigger(children=["Is it accessible?"]),
                AccordionContent(children=[Text("Yes. It adheres to the WAI-ARIA spec.")]),
            ],
        )
        ```

    Args:
        value: Unique identifier for this item within the :class:`Accordion`.
            Used by the parent to track open/closed state.
        children: Exactly one :class:`AccordionTrigger` and one
            :class:`AccordionContent`.
        id: Optional HTML element id.
        class_name: Additional CSS class names.
    """

    component_type: str = "AccordionItem"

    def __init__(
        self,
        value: str,
        children: ChildrenType = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.value = value
        self.add_children(children)

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
    """
    Clickable header that toggles an :class:`AccordionItem`.

    Renders as a button with a rotating chevron indicator. Must be placed
    inside an :class:`AccordionItem`.

    Example:
        ```python
        AccordionTrigger(children=["Frequently Asked Questions"])
        ```

    Args:
        children: Trigger label — typically a string.
        id: Optional HTML element id.
        class_name: Additional CSS class names.
    """

    component_type: str = "AccordionTrigger"

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


class AccordionContent(Component):
    """
    Revealed body of an :class:`AccordionItem`.

    Hidden when the item is collapsed; animated into view when the
    corresponding :class:`AccordionTrigger` is activated.

    Example:
        ```python
        AccordionContent(
            children=[Text("Yes. It adheres to the WAI-ARIA spec.")]
        )
        ```

    Args:
        children: Content shown when the accordion item is open.
        id: Optional HTML element id.
        class_name: Additional CSS class names.
    """

    component_type: str = "AccordionContent"

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
