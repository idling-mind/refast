"""Navigation components based on shadcn/ui."""

from typing import Any, Literal, Union

from refast.components.base import Component


class Breadcrumb(Component):
    """
    A navigation component showing the current page location.

    Example:
        ```python
        Breadcrumb(
            children=[
                BreadcrumbItem(BreadcrumbLink("Home", href="/")),
                BreadcrumbSeparator(),
                BreadcrumbItem(BreadcrumbPage("Current Page")),
            ]
        )
        ```
    """

    component_type: str = "Breadcrumb"

    def __init__(
        self,
        children: list["Component"] | None = None,
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


class BreadcrumbList(Component):
    """Container for breadcrumb items."""

    component_type: str = "BreadcrumbList"

    def __init__(
        self,
        children: list["Component"] | None = None,
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


class BreadcrumbItem(Component):
    """A single breadcrumb item."""

    component_type: str = "BreadcrumbItem"

    def __init__(
        self,
        children: Union[list["Component"], "Component", str, None] = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            if isinstance(children, list):
                self._children = children
            else:
                self._children = [children]

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


class BreadcrumbLink(Component):
    """A clickable breadcrumb link."""

    component_type: str = "BreadcrumbLink"

    def __init__(
        self,
        label: str,
        href: str = "#",
        on_click: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.label = label
        self.href = href
        self.on_click = on_click

    def render(self) -> dict[str, Any]:
        props = {
            "href": self.href,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.on_click:
            props["on_click"] = self.on_click.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": [self.label],
        }


class BreadcrumbPage(Component):
    """The current page indicator (non-clickable)."""

    component_type: str = "BreadcrumbPage"

    def __init__(
        self,
        label: str,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.label = label

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [self.label],
        }


class BreadcrumbSeparator(Component):
    """A separator between breadcrumb items."""

    component_type: str = "BreadcrumbSeparator"

    def __init__(
        self,
        children: Union[list["Component"], "Component", str, None] = None,
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


class BreadcrumbEllipsis(Component):
    """An ellipsis for collapsed breadcrumbs."""

    component_type: str = "BreadcrumbEllipsis"

    def __init__(
        self,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [],
        }


class NavigationMenu(Component):
    """
    A collection of links for navigating websites.

    Example:
        ```python
        NavigationMenu(
            children=[
                NavigationMenuList(
                    children=[
                        NavigationMenuItem(
                            NavigationMenuTrigger("Getting Started"),
                            NavigationMenuContent(
                                Link("Introduction", href="/docs"),
                            ),
                        ),
                    ]
                ),
            ]
        )
        ```
    """

    component_type: str = "NavigationMenu"

    def __init__(
        self,
        children: list["Component"] | None = None,
        orientation: Literal["horizontal", "vertical"] = "horizontal",
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.orientation = orientation
        if children:
            self._children = children

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "orientation": self.orientation,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class NavigationMenuList(Component):
    """Container for navigation menu items."""

    component_type: str = "NavigationMenuList"

    def __init__(
        self,
        children: list["Component"] | None = None,
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


class NavigationMenuItem(Component):
    """A single navigation menu item."""

    component_type: str = "NavigationMenuItem"

    def __init__(
        self,
        children: Union[list["Component"], "Component", None] = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            if isinstance(children, list):
                self._children = children
            else:
                self._children = [children]

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


class NavigationMenuTrigger(Component):
    """A trigger button that opens the navigation content."""

    component_type: str = "NavigationMenuTrigger"

    def __init__(
        self,
        label: str,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.label = label

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [self.label],
        }


class NavigationMenuContent(Component):
    """The content that appears when a trigger is activated."""

    component_type: str = "NavigationMenuContent"

    def __init__(
        self,
        children: Union[list["Component"], "Component", None] = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            if isinstance(children, list):
                self._children = children
            else:
                self._children = [children]

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


class NavigationMenuLink(Component):
    """A link within the navigation menu."""

    component_type: str = "NavigationMenuLink"

    def __init__(
        self,
        label: str,
        href: str = "#",
        active: bool = False,
        on_click: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.label = label
        self.href = href
        self.active = active
        self.on_click = on_click

    def render(self) -> dict[str, Any]:
        props = {
            "href": self.href,
            "active": self.active,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.on_click:
            props["on_click"] = self.on_click.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": [self.label],
        }


class Pagination(Component):
    """
    A component for paginating through content.

    Example:
        ```python
        Pagination(
            children=[
                PaginationContent(
                    children=[
                        PaginationItem(PaginationPrevious(href="#")),
                        PaginationItem(PaginationLink("1", href="#", active=True)),
                        PaginationItem(PaginationLink("2", href="#")),
                        PaginationItem(PaginationEllipsis()),
                        PaginationItem(PaginationNext(href="#")),
                    ]
                )
            ]
        )
        ```
    """

    component_type: str = "Pagination"

    def __init__(
        self,
        children: list["Component"] | None = None,
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


class PaginationContent(Component):
    """Container for pagination items."""

    component_type: str = "PaginationContent"

    def __init__(
        self,
        children: list["Component"] | None = None,
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


class PaginationItem(Component):
    """A single pagination item."""

    component_type: str = "PaginationItem"

    def __init__(
        self,
        children: Union[list["Component"], "Component", None] = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            if isinstance(children, list):
                self._children = children
            else:
                self._children = [children]

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


class PaginationLink(Component):
    """A pagination link to a specific page."""

    component_type: str = "PaginationLink"

    def __init__(
        self,
        label: str,
        href: str = "#",
        active: bool = False,
        on_click: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.label = label
        self.href = href
        self.active = active
        self.on_click = on_click

    def render(self) -> dict[str, Any]:
        props = {
            "href": self.href,
            "active": self.active,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.on_click:
            props["on_click"] = self.on_click.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": [self.label],
        }


class PaginationPrevious(Component):
    """Previous page button."""

    component_type: str = "PaginationPrevious"

    def __init__(
        self,
        href: str = "#",
        on_click: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.href = href
        self.on_click = on_click

    def render(self) -> dict[str, Any]:
        props = {
            "href": self.href,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.on_click:
            props["on_click"] = self.on_click.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": [],
        }


class PaginationNext(Component):
    """Next page button."""

    component_type: str = "PaginationNext"

    def __init__(
        self,
        href: str = "#",
        on_click: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.href = href
        self.on_click = on_click

    def render(self) -> dict[str, Any]:
        props = {
            "href": self.href,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.on_click:
            props["on_click"] = self.on_click.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": [],
        }


class PaginationEllipsis(Component):
    """Ellipsis indicator for skipped pages."""

    component_type: str = "PaginationEllipsis"

    def __init__(
        self,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [],
        }


class Menubar(Component):
    """
    A visually persistent menu common in desktop applications.

    Example:
        ```python
        Menubar(
            children=[
                MenubarMenu(
                    MenubarTrigger("File"),
                    MenubarContent(
                        children=[
                            MenubarItem("New Tab", shortcut="⌘T"),
                            MenubarItem("New Window", shortcut="⌘N"),
                        ]
                    ),
                ),
            ]
        )
        ```
    """

    component_type: str = "Menubar"

    def __init__(
        self,
        children: list["Component"] | None = None,
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


class MenubarMenu(Component):
    """A single menu within the menubar."""

    component_type: str = "MenubarMenu"

    def __init__(
        self,
        trigger: "Component | None" = None,
        content: "Component | None" = None,
        children: list["Component"] | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if trigger and content:
            self._children = [trigger, content]
        elif children:
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


class MenubarTrigger(Component):
    """The button that opens a menu."""

    component_type: str = "MenubarTrigger"

    def __init__(
        self,
        label: str,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.label = label

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [self.label],
        }


class MenubarContent(Component):
    """The content of a menu."""

    component_type: str = "MenubarContent"

    def __init__(
        self,
        children: list["Component"] | None = None,
        align: Literal["start", "center", "end"] = "start",
        side_offset: int = 5,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.align = align
        self.side_offset = side_offset
        if children:
            self._children = children

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "align": self.align,
                "sideOffset": self.side_offset,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class MenubarItem(Component):
    """A menu item."""

    component_type: str = "MenubarItem"

    def __init__(
        self,
        label: str,
        shortcut: str | None = None,
        disabled: bool = False,
        on_select: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.label = label
        self.shortcut = shortcut
        self.disabled = disabled
        self.on_select = on_select

    def render(self) -> dict[str, Any]:
        props = {
            "shortcut": self.shortcut,
            "disabled": self.disabled,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.on_select:
            props["on_select"] = self.on_select.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": [self.label],
        }


class MenubarSeparator(Component):
    """A separator line in the menu."""

    component_type: str = "MenubarSeparator"

    def __init__(
        self,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [],
        }


class MenubarCheckboxItem(Component):
    """A checkbox menu item."""

    component_type: str = "MenubarCheckboxItem"

    def __init__(
        self,
        label: str,
        checked: bool = False,
        on_checked_change: Any = None,
        disabled: bool = False,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.label = label
        self.checked = checked
        self.on_checked_change = on_checked_change
        self.disabled = disabled

    def render(self) -> dict[str, Any]:
        props = {
            "checked": self.checked,
            "disabled": self.disabled,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.on_checked_change:
            props["on_checked_change"] = self.on_checked_change.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": [self.label],
        }


class MenubarRadioGroup(Component):
    """A group of radio menu items."""

    component_type: str = "MenubarRadioGroup"

    def __init__(
        self,
        value: str = "",
        on_value_change: Any = None,
        children: list["Component"] | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.value = value
        self.on_value_change = on_value_change
        if children:
            self._children = children

    def render(self) -> dict[str, Any]:
        props = {
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


class MenubarRadioItem(Component):
    """A radio menu item."""

    component_type: str = "MenubarRadioItem"

    def __init__(
        self,
        label: str,
        value: str = "",
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.label = label
        self.value = value

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "value": self.value,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [self.label],
        }


class MenubarSub(Component):
    """A submenu container."""

    component_type: str = "MenubarSub"

    def __init__(
        self,
        children: list["Component"] | None = None,
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


class MenubarSubTrigger(Component):
    """A trigger for a submenu."""

    component_type: str = "MenubarSubTrigger"

    def __init__(
        self,
        label: str,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.label = label

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [self.label],
        }


class MenubarSubContent(Component):
    """The content of a submenu."""

    component_type: str = "MenubarSubContent"

    def __init__(
        self,
        children: list["Component"] | None = None,
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


class Command(Component):
    """
    A command menu component (CMD+K style).

    Example:
        ```python
        Command(
            children=[
                CommandInput(placeholder="Type a command..."),
                CommandList(
                    children=[
                        CommandEmpty("No results found."),
                        CommandGroup(
                            heading="Suggestions",
                            children=[
                                CommandItem("Calendar", icon="Calendar"),
                            ]
                        ),
                    ]
                ),
            ]
        )
        ```
    """

    component_type: str = "Command"

    def __init__(
        self,
        children: list["Component"] | None = None,
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


class CommandInput(Component):
    """The input for the command menu."""

    component_type: str = "CommandInput"

    def __init__(
        self,
        placeholder: str = "Search...",
        value: str | None = None,
        on_value_change: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.placeholder = placeholder
        self.value = value
        self.on_value_change = on_value_change

    def render(self) -> dict[str, Any]:
        props = {
            "placeholder": self.placeholder,
            "on_value_change": self.on_value_change.serialize() if self.on_value_change else None,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.value is not None:
            props["value"] = self.value

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": [],
        }


class CommandList(Component):
    """The list container for command items."""

    component_type: str = "CommandList"

    def __init__(
        self,
        children: list["Component"] | None = None,
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


class CommandEmpty(Component):
    """Message shown when no results are found."""

    component_type: str = "CommandEmpty"

    def __init__(
        self,
        message: str = "No results found.",
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.message = message

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [self.message],
        }


class CommandGroup(Component):
    """A group of command items."""

    component_type: str = "CommandGroup"

    def __init__(
        self,
        heading: str = "",
        children: list["Component"] | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.heading = heading
        if children:
            self._children = children

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "heading": self.heading,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class CommandItem(Component):
    """A single command item."""

    component_type: str = "CommandItem"

    def __init__(
        self,
        label: str,
        icon: str | None = None,
        value: str | None = None,
        disabled: bool = False,
        on_select: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.label = label
        self.icon = icon
        self.value = value or label
        self.disabled = disabled
        self.on_select = on_select

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "icon": self.icon,
                "value": self.value,
                "disabled": self.disabled,
                "on_select": self.on_select.serialize() if self.on_select else None,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [self.label],
        }


class CommandSeparator(Component):
    """A separator between command groups."""

    component_type: str = "CommandSeparator"

    def __init__(
        self,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [],
        }


class CommandShortcut(Component):
    """A keyboard shortcut indicator."""

    component_type: str = "CommandShortcut"

    def __init__(
        self,
        shortcut: str,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.shortcut = shortcut

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [self.shortcut],
        }


class Sidebar(Component):
    """
    A composable sidebar component.

    Example:
        ```python
        Sidebar(
            children=[
                SidebarHeader(...),
                SidebarContent(
                    SidebarGroup(
                        SidebarGroupLabel("Application"),
                        SidebarGroupContent(
                            SidebarMenu(
                                SidebarMenuItem(
                                    SidebarMenuButton("Dashboard", icon="Home")
                                ),
                            ),
                        ),
                    ),
                ),
                SidebarFooter(...),
            ]
        )
        ```
    """

    component_type: str = "Sidebar"

    def __init__(
        self,
        children: list["Component"] | None = None,
        side: Literal["left", "right"] = "left",
        variant: Literal["sidebar", "floating", "inset"] = "sidebar",
        collapsible: Literal["offcanvas", "icon", "none"] = "offcanvas",
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.side = side
        self.variant = variant
        self.collapsible = collapsible
        if children:
            self._children = children

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "side": self.side,
                "variant": self.variant,
                "collapsible": self.collapsible,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class SidebarHeader(Component):
    """The header section of the sidebar."""

    component_type: str = "SidebarHeader"

    def __init__(
        self,
        children: list["Component"] | None = None,
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


class SidebarContent(Component):
    """The main content area of the sidebar."""

    component_type: str = "SidebarContent"

    def __init__(
        self,
        children: list["Component"] | None = None,
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


class SidebarFooter(Component):
    """The footer section of the sidebar."""

    component_type: str = "SidebarFooter"

    def __init__(
        self,
        children: list["Component"] | None = None,
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


class SidebarGroup(Component):
    """A group of related sidebar items."""

    component_type: str = "SidebarGroup"

    def __init__(
        self,
        children: list["Component"] | None = None,
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


class SidebarGroupLabel(Component):
    """A label for a sidebar group."""

    component_type: str = "SidebarGroupLabel"

    def __init__(
        self,
        label: str,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.label = label

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [self.label],
        }


class SidebarGroupContent(Component):
    """The content of a sidebar group."""

    component_type: str = "SidebarGroupContent"

    def __init__(
        self,
        children: list["Component"] | None = None,
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


class SidebarMenu(Component):
    """A menu within the sidebar."""

    component_type: str = "SidebarMenu"

    def __init__(
        self,
        children: list["Component"] | None = None,
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


class SidebarMenuItem(Component):
    """A single menu item."""

    component_type: str = "SidebarMenuItem"

    def __init__(
        self,
        children: Union[list["Component"], "Component", None] = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            if isinstance(children, list):
                self._children = children
            else:
                self._children = [children]

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


class SidebarMenuButton(Component):
    """A button in the sidebar menu."""

    component_type: str = "SidebarMenuButton"

    def __init__(
        self,
        label: str,
        icon: str | None = None,
        active: bool = False,
        on_click: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.label = label
        self.icon = icon
        self.active = active
        self.on_click = on_click

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "icon": self.icon,
                "active": self.active,
                "on_click": self.on_click.serialize() if self.on_click else None,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [self.label],
        }


class SidebarTrigger(Component):
    """A button to toggle the sidebar."""

    component_type: str = "SidebarTrigger"

    def __init__(
        self,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [],
        }

