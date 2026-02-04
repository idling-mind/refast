"""Navigation components based on shadcn/ui."""

from typing import Any, Literal, Union

from refast.components.base import Component
from refast.components.shadcn.icon import Icon


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
                "side_offset": self.side_offset,
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


class SidebarProvider(Component):
    """
    Provides context for sidebar state management.

    The SidebarProvider component wraps your application and provides
    the sidebar context to all child components. It handles:
    - Collapsible state (open/closed)
    - Mobile responsiveness
    - Keyboard shortcuts (Ctrl/Cmd+B)

    Example:
        ```python
        SidebarProvider(
            children=[
                Sidebar(...),
                SidebarInset(
                    children=[
                        SidebarTrigger(),
                        # Your main content
                    ]
                ),
            ]
        )
        ```

    Args:
        default_open: Initial open state of the sidebar (default: True)
        children: Child components
    """

    component_type: str = "SidebarProvider"

    def __init__(
        self,
        children: list["Component"] | None = None,
        default_open: bool = True,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.default_open = default_open
        if children:
            self._children = children

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "default_open": self.default_open,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class Sidebar(Component):
    """
    A composable, themeable and customizable sidebar component.

    The Sidebar component is the main container for the sidebar navigation.
    It supports different variants, sides, and collapsible modes.

    Example:
        ```python
        Sidebar(
            side="left",
            variant="sidebar",
            collapsible="icon",
            children=[
                SidebarHeader(...),
                SidebarContent(
                    SidebarGroup(
                        SidebarGroupLabel("Application"),
                        SidebarGroupContent(
                            SidebarMenu(
                                SidebarMenuItem(
                                    SidebarMenuButton("Dashboard", icon="🏠")
                                ),
                            ),
                        ),
                    ),
                ),
                SidebarFooter(...),
                SidebarRail(),
            ]
        )
        ```

    Args:
        side: The side of the sidebar ("left" or "right")
        variant: The variant style ("sidebar", "floating", or "inset")
        collapsible: Collapsible mode ("offcanvas", "icon", or "none")
        children: Child components
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


class SidebarInset(Component):
    """
    The main content area when using inset variant sidebar.

    Use SidebarInset to wrap your main content when using `variant="inset"`.
    It provides proper spacing and styling for the inset layout.

    Example:
        ```python
        SidebarProvider(
            children=[
                Sidebar(variant="inset", ...),
                SidebarInset(
                    children=[
                        SidebarTrigger(),
                        # Main content here
                    ]
                ),
            ]
        )
        ```
    """

    component_type: str = "SidebarInset"

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


class SidebarHeader(Component):
    """
    The header section of the sidebar.

    Use SidebarHeader for branding, workspace selectors, or other
    content that should stick to the top of the sidebar.

    Example:
        ```python
        SidebarHeader(
            children=[
                Text("My Application", class_name="text-lg font-bold"),
            ]
        )
        ```
    """

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
    """
    The main scrollable content area of the sidebar.

    SidebarContent is where you place your SidebarGroup components.
    It automatically handles overflow scrolling.

    Example:
        ```python
        SidebarContent(
            children=[
                SidebarGroup(...),
                SidebarGroup(...),
            ]
        )
        ```
    """

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
    """
    The footer section of the sidebar.

    Use SidebarFooter for user menus, settings, or other content
    that should stick to the bottom of the sidebar.

    Example:
        ```python
        SidebarFooter(
            children=[
                SidebarMenu(
                    children=[
                        SidebarMenuItem(
                            children=[
                                SidebarMenuButton("Settings", icon="⚙️")
                            ]
                        )
                    ]
                )
            ]
        )
        ```
    """

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


class SidebarSeparator(Component):
    """A visual separator within the sidebar."""

    component_type: str = "SidebarSeparator"

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


class SidebarGroup(Component):
    """
    A group of related sidebar items.

    Use SidebarGroup to organize menu items into logical sections.
    Each group can have a label and optional action button.

    Example:
        ```python
        SidebarGroup(
            children=[
                SidebarGroupLabel("Projects"),
                SidebarGroupAction(icon="➕", title="Add Project"),
                SidebarGroupContent(
                    children=[
                        SidebarMenu(...)
                    ]
                )
            ]
        )
        ```
    """

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
    """
    A label for a sidebar group.

    Example:
        ```python
        SidebarGroupLabel("Navigation")
        ```
    """

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


class SidebarGroupAction(Component):
    """
    An action button for a sidebar group (appears next to the label).

    Example:
        ```python
        # Using Lucide icon name
        SidebarGroupAction(
            icon="plus",
            title="Add Item",
            on_click=ctx.callback(handle_add)
        )

        # Backward compatible with emoji
        SidebarGroupAction(
            icon="➕",
            title="Add Item",
            on_click=ctx.callback(handle_add)
        )
        ```
    """

    component_type: str = "SidebarGroupAction"

    def __init__(
        self,
        icon: str | None = None,
        title: str | None = None,
        on_click: Any = None,
        children: list["Component"] | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.icon = icon
        self.title = title
        self.on_click = on_click
        if children:
            self._children = children

    def render(self) -> dict[str, Any]:
        children = self._render_children()
        if self.icon and not children:
            # Create an Icon component for the icon
            icon_component = Icon(self.icon, size=16)
            children = [icon_component.render()]
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "title": self.title,
                "onClick": self.on_click.serialize() if self.on_click else None,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": children,
        }


class SidebarGroupContent(Component):
    """
    The content container of a sidebar group.

    Example:
        ```python
        SidebarGroupContent(
            children=[
                SidebarMenu(...)
            ]
        )
        ```
    """

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
    """
    A menu container within the sidebar.

    Example:
        ```python
        SidebarMenu(
            children=[
                SidebarMenuItem(...),
                SidebarMenuItem(...),
            ]
        )
        ```
    """

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
    """
    A single menu item container.

    Example:
        ```python
        SidebarMenuItem(
            children=[
                SidebarMenuButton("Dashboard", icon="🏠", is_active=True)
            ]
        )
        ```
    """

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
    """
    A clickable button in the sidebar menu.

    Example:
        ```python
        # Using Lucide icon name
        SidebarMenuButton(
            "Dashboard",
            icon="home",
            is_active=True,
            on_click=ctx.callback(handle_click)
        )

        # Backward compatible with emoji
        SidebarMenuButton(
            "Settings",
            icon="⚙️",
            on_click=ctx.callback(handle_settings)
        )
        ```

    Args:
        label: The button text
        icon: Optional Lucide icon name (e.g., "home", "settings") or emoji for backward compatibility
        is_active: Whether the button is currently active
        variant: "default" or "outline"
        size: "default", "sm", or "lg"
        href: Optional URL to link to
        on_click: Optional click callback
    """

    component_type: str = "SidebarMenuButton"

    def __init__(
        self,
        label: str,
        icon: str | None = None,
        is_active: bool = False,
        variant: Literal["default", "outline"] = "default",
        size: Literal["default", "sm", "lg"] = "default",
        href: str | None = None,
        on_click: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.label = label
        self.icon = icon
        self.is_active = is_active
        self.variant = variant
        self.size = size
        self.href = href
        self.on_click = on_click

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "icon": self.icon,
                "is_active": self.is_active,
                "variant": self.variant,
                "size": self.size,
                "href": self.href,
                "onClick": self.on_click.serialize() if self.on_click else None,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [self.label],
        }


class SidebarMenuAction(Component):
    """
    An action button within a menu item.

    Works independently of SidebarMenuButton, allowing the menu button
    to be a link while the action button triggers a different action.

    Example:
        ```python
        SidebarMenuItem(
            children=[
                SidebarMenuButton("Project", href="/project"),
                # Using Lucide icon name
                SidebarMenuAction(
                    icon="more-vertical",
                    on_click=ctx.callback(handle_options)
                )
            ]
        )
        ```
    """

    component_type: str = "SidebarMenuAction"

    def __init__(
        self,
        icon: str | None = None,
        show_on_hover: bool = False,
        on_click: Any = None,
        children: list["Component"] | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.icon = icon
        self.show_on_hover = show_on_hover
        self.on_click = on_click
        if children:
            self._children = children

    def render(self) -> dict[str, Any]:
        children = self._render_children()
        if self.icon and not children:
            # Create an Icon component for the icon
            icon_component = Icon(self.icon, size=16)
            children = [icon_component.render()]
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "show_on_hover": self.show_on_hover,
                "onClick": self.on_click.serialize() if self.on_click else None,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": children,
        }


class SidebarMenuBadge(Component):
    """
    A badge displayed on a menu item.

    Example:
        ```python
        SidebarMenuItem(
            children=[
                SidebarMenuButton("Inbox"),
                SidebarMenuBadge("24")
            ]
        )
        ```
    """

    component_type: str = "SidebarMenuBadge"

    def __init__(
        self,
        badge: str,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.badge = badge

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [self.badge],
        }


class SidebarMenuSub(Component):
    """
    A submenu container for nested menu items.

    Example:
        ```python
        SidebarMenuItem(
            children=[
                SidebarMenuButton("Settings"),
                SidebarMenuSub(
                    children=[
                        SidebarMenuSubItem(
                            children=[SidebarMenuSubButton("General")]
                        ),
                        SidebarMenuSubItem(
                            children=[SidebarMenuSubButton("Security")]
                        ),
                    ]
                )
            ]
        )
        ```
    """

    component_type: str = "SidebarMenuSub"

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


class SidebarMenuSubItem(Component):
    """A submenu item container."""

    component_type: str = "SidebarMenuSubItem"

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


class SidebarMenuSubButton(Component):
    """
    A button for submenu items.

    Example:
        ```python
        SidebarMenuSubButton("General Settings", is_active=True)
        ```
    """

    component_type: str = "SidebarMenuSubButton"

    def __init__(
        self,
        label: str,
        is_active: bool = False,
        size: Literal["sm", "md"] = "md",
        href: str | None = None,
        on_click: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.label = label
        self.is_active = is_active
        self.size = size
        self.href = href
        self.on_click = on_click

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "is_active": self.is_active,
                "size": self.size,
                "href": self.href,
                "onClick": self.on_click.serialize() if self.on_click else None,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [self.label],
        }


class SidebarMenuSkeleton(Component):
    """
    A skeleton loader for menu items.

    Example:
        ```python
        SidebarMenu(
            children=[
                SidebarMenuItem(SidebarMenuSkeleton(show_icon=True))
                for _ in range(5)
            ]
        )
        ```
    """

    component_type: str = "SidebarMenuSkeleton"

    def __init__(
        self,
        show_icon: bool = False,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.show_icon = show_icon

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "show_icon": self.show_icon,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [],
        }


class SidebarRail(Component):
    """
    A rail for toggling the sidebar by dragging or clicking.

    Add SidebarRail to the end of your Sidebar to enable edge toggling.

    Example:
        ```python
        Sidebar(
            children=[
                SidebarHeader(...),
                SidebarContent(...),
                SidebarFooter(...),
                SidebarRail(),  # Add at the end
            ]
        )
        ```
    """

    component_type: str = "SidebarRail"

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


class SidebarTrigger(Component):
    """
    A button to toggle the sidebar open/closed.

    Example:
        ```python
        SidebarTrigger()  # Uses default toggle behavior
        ```
    """

    component_type: str = "SidebarTrigger"

    def __init__(
        self,
        on_click: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.on_click = on_click

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "onClick": self.on_click.serialize() if self.on_click else None,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [],
        }


