"""Overlay components based on shadcn/ui."""

from typing import Any, Literal, Union

from refast.components.base import Component


class AlertDialog(Component):
    """
    A modal dialog that interrupts the user with important content.

    Example:
        ```python
        AlertDialog(
            open=show_dialog,
            on_open_change=ctx.callback(handle_dialog_change),
            children=[
                AlertDialogTrigger(Button("Delete")),
                AlertDialogContent(
                    AlertDialogHeader(
                        AlertDialogTitle("Are you absolutely sure?"),
                        AlertDialogDescription("This action cannot be undone."),
                    ),
                    AlertDialogFooter(
                        AlertDialogCancel("Cancel"),
                        AlertDialogAction("Continue"),
                    ),
                ),
            ]
        )
        ```
    """

    component_type: str = "AlertDialog"

    def __init__(
        self,
        open: bool | None = None,
        default_open: bool = False,
        on_open_change: Any = None,
        children: list["Component"] | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.open = open
        self.default_open = default_open
        self.on_open_change = on_open_change
        if children:
            self._children = children

    def render(self) -> dict[str, Any]:
        props = {
            "defaultOpen": self.default_open,
            "className": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.open is not None:
            props["open"] = self.open
        if self.on_open_change:
            props["onOpenChange"] = self.on_open_change.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": self._render_children(),
        }


class AlertDialogTrigger(Component):
    """The button that opens the alert dialog."""

    component_type: str = "AlertDialogTrigger"

    def __init__(
        self,
        children: Union[list["Component"], "Component", None] = None,
        as_child: bool = False,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.as_child = as_child
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
                "asChild": self.as_child,
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class AlertDialogContent(Component):
    """The content of the alert dialog."""

    component_type: str = "AlertDialogContent"

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
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class AlertDialogHeader(Component):
    """The header section of the alert dialog."""

    component_type: str = "AlertDialogHeader"

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
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class AlertDialogFooter(Component):
    """The footer section of the alert dialog."""

    component_type: str = "AlertDialogFooter"

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
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class AlertDialogTitle(Component):
    """The title of the alert dialog."""

    component_type: str = "AlertDialogTitle"

    def __init__(
        self,
        title: str,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.title = title

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [self.title],
        }


class AlertDialogDescription(Component):
    """The description of the alert dialog."""

    component_type: str = "AlertDialogDescription"

    def __init__(
        self,
        description: str,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.description = description

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [self.description],
        }


class AlertDialogAction(Component):
    """The confirm action button."""

    component_type: str = "AlertDialogAction"

    def __init__(
        self,
        label: str,
        on_click: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.label = label
        self.on_click = on_click

    def render(self) -> dict[str, Any]:
        props = {
            "className": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.on_click:
            props["onClick"] = self.on_click.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": [self.label],
        }


class AlertDialogCancel(Component):
    """The cancel action button."""

    component_type: str = "AlertDialogCancel"

    def __init__(
        self,
        label: str = "Cancel",
        on_click: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.label = label
        self.on_click = on_click

    def render(self) -> dict[str, Any]:
        props = {
            "className": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.on_click:
            props["onClick"] = self.on_click.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": [self.label],
        }


class Sheet(Component):
    """
    A panel that slides out from the edge of the screen.

    Example:
        ```python
        Sheet(
            side="right",
            children=[
                SheetTrigger(Button("Open")),
                SheetContent(
                    SheetHeader(
                        SheetTitle("Edit Profile"),
                        SheetDescription("Make changes to your profile."),
                    ),
                    # Form content
                    SheetFooter(Button("Save changes")),
                ),
            ]
        )
        ```
    """

    component_type: str = "Sheet"

    def __init__(
        self,
        open: bool | None = None,
        default_open: bool = False,
        on_open_change: Any = None,
        children: list["Component"] | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.open = open
        self.default_open = default_open
        self.on_open_change = on_open_change
        if children:
            self._children = children

    def render(self) -> dict[str, Any]:
        props = {
            "defaultOpen": self.default_open,
            "className": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.open is not None:
            props["open"] = self.open
        if self.on_open_change:
            props["onOpenChange"] = self.on_open_change.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": self._render_children(),
        }


class SheetTrigger(Component):
    """The button that opens the sheet."""

    component_type: str = "SheetTrigger"

    def __init__(
        self,
        children: Union[list["Component"], "Component", None] = None,
        as_child: bool = False,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.as_child = as_child
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
                "asChild": self.as_child,
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class SheetClose(Component):
    """A button to close the sheet."""

    component_type: str = "SheetClose"

    def __init__(
        self,
        children: Union[list["Component"], "Component", None] = None,
        as_child: bool = False,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.as_child = as_child
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
                "asChild": self.as_child,
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class SheetContent(Component):
    """The content of the sheet."""

    component_type: str = "SheetContent"

    def __init__(
        self,
        children: Union[list["Component"], "Component", None] = None,
        side: Literal["top", "right", "bottom", "left"] = "right",
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.side = side
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
                "side": self.side,
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class SheetHeader(Component):
    """The header section of the sheet."""

    component_type: str = "SheetHeader"

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
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class SheetFooter(Component):
    """The footer section of the sheet."""

    component_type: str = "SheetFooter"

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
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class SheetTitle(Component):
    """The title of the sheet."""

    component_type: str = "SheetTitle"

    def __init__(
        self,
        title: str,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.title = title

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [self.title],
        }


class SheetDescription(Component):
    """The description of the sheet."""

    component_type: str = "SheetDescription"

    def __init__(
        self,
        description: str,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.description = description

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [self.description],
        }


class Popover(Component):
    """
    Displays rich content in a portal, triggered by a button.

    Example:
        ```python
        Popover(
            children=[
                PopoverTrigger(Button("Open popover")),
                PopoverContent(
                    Heading("Dimensions", level=4),
                    Paragraph("Set the dimensions."),
                ),
            ]
        )
        ```
    """

    component_type: str = "Popover"

    def __init__(
        self,
        open: bool | None = None,
        default_open: bool = False,
        on_open_change: Any = None,
        children: list["Component"] | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.open = open
        self.default_open = default_open
        self.on_open_change = on_open_change
        if children:
            self._children = children

    def render(self) -> dict[str, Any]:
        props = {
            "defaultOpen": self.default_open,
            "className": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.open is not None:
            props["open"] = self.open
        if self.on_open_change:
            props["onOpenChange"] = self.on_open_change.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": self._render_children(),
        }


class PopoverTrigger(Component):
    """The button that opens the popover."""

    component_type: str = "PopoverTrigger"

    def __init__(
        self,
        children: Union[list["Component"], "Component", None] = None,
        as_child: bool = False,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.as_child = as_child
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
                "asChild": self.as_child,
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class PopoverContent(Component):
    """The content of the popover."""

    component_type: str = "PopoverContent"

    def __init__(
        self,
        children: Union[list["Component"], "Component", None] = None,
        side: Literal["top", "right", "bottom", "left"] = "bottom",
        side_offset: int = 4,
        align: Literal["start", "center", "end"] = "center",
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.side = side
        self.side_offset = side_offset
        self.align = align
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
                "side": self.side,
                "sideOffset": self.side_offset,
                "align": self.align,
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class HoverCard(Component):
    """
    For sighted users to preview content behind a link.

    Example:
        ```python
        HoverCard(
            children=[
                HoverCardTrigger(Link("@shadcn", href="#")),
                HoverCardContent(
                    Avatar(src="...", alt="@shadcn"),
                ),
            ]
        )
        ```
    """

    component_type: str = "HoverCard"

    def __init__(
        self,
        open: bool | None = None,
        default_open: bool = False,
        on_open_change: Any = None,
        open_delay: int = 700,
        close_delay: int = 300,
        children: list["Component"] | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.open = open
        self.default_open = default_open
        self.on_open_change = on_open_change
        self.open_delay = open_delay
        self.close_delay = close_delay
        if children:
            self._children = children

    def render(self) -> dict[str, Any]:
        props = {
            "defaultOpen": self.default_open,
            "openDelay": self.open_delay,
            "closeDelay": self.close_delay,
            "className": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.open is not None:
            props["open"] = self.open
        if self.on_open_change:
            props["onOpenChange"] = self.on_open_change.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": self._render_children(),
        }


class HoverCardTrigger(Component):
    """The element that triggers the hover card."""

    component_type: str = "HoverCardTrigger"

    def __init__(
        self,
        children: Union[list["Component"], "Component", None] = None,
        as_child: bool = False,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.as_child = as_child
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
                "asChild": self.as_child,
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class HoverCardContent(Component):
    """The content of the hover card."""

    component_type: str = "HoverCardContent"

    def __init__(
        self,
        children: Union[list["Component"], "Component", None] = None,
        side: Literal["top", "right", "bottom", "left"] = "bottom",
        side_offset: int = 4,
        align: Literal["start", "center", "end"] = "center",
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.side = side
        self.side_offset = side_offset
        self.align = align
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
                "side": self.side,
                "sideOffset": self.side_offset,
                "align": self.align,
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class DropdownMenu(Component):
    """
    Displays a menu to the user, triggered by a button.

    Example:
        ```python
        DropdownMenu(
            children=[
                DropdownMenuTrigger(Button("Open")),
                DropdownMenuContent(
                    DropdownMenuLabel("My Account"),
                    DropdownMenuSeparator(),
                    DropdownMenuItem("Profile", shortcut="⇧⌘P"),
                ),
            ]
        )
        ```
    """

    component_type: str = "DropdownMenu"

    def __init__(
        self,
        open: bool | None = None,
        default_open: bool = False,
        on_open_change: Any = None,
        children: list["Component"] | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.open = open
        self.default_open = default_open
        self.on_open_change = on_open_change
        if children:
            self._children = children

    def render(self) -> dict[str, Any]:
        props = {
            "defaultOpen": self.default_open,
            "className": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.open is not None:
            props["open"] = self.open
        if self.on_open_change:
            props["onOpenChange"] = self.on_open_change.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": self._render_children(),
        }


class DropdownMenuTrigger(Component):
    """The button that opens the dropdown menu."""

    component_type: str = "DropdownMenuTrigger"

    def __init__(
        self,
        children: Union[list["Component"], "Component", None] = None,
        as_child: bool = False,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.as_child = as_child
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
                "asChild": self.as_child,
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class DropdownMenuContent(Component):
    """The content of the dropdown menu."""

    component_type: str = "DropdownMenuContent"

    def __init__(
        self,
        children: list["Component"] | None = None,
        side: Literal["top", "right", "bottom", "left"] = "bottom",
        side_offset: int = 4,
        align: Literal["start", "center", "end"] = "start",
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.side = side
        self.side_offset = side_offset
        self.align = align
        if children:
            self._children = children

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "side": self.side,
                "sideOffset": self.side_offset,
                "align": self.align,
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class DropdownMenuItem(Component):
    """A menu item in the dropdown."""

    component_type: str = "DropdownMenuItem"

    def __init__(
        self,
        label: str,
        icon: str | None = None,
        shortcut: str | None = None,
        disabled: bool = False,
        on_select: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.label = label
        self.icon = icon
        self.shortcut = shortcut
        self.disabled = disabled
        self.on_select = on_select

    def render(self) -> dict[str, Any]:
        props = {
            "icon": self.icon,
            "shortcut": self.shortcut,
            "disabled": self.disabled,
            "className": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.on_select:
            props["onSelect"] = self.on_select.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": [self.label],
        }


class DropdownMenuLabel(Component):
    """A label in the dropdown menu."""

    component_type: str = "DropdownMenuLabel"

    def __init__(
        self,
        label: str,
        inset: bool = False,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.label = label
        self.inset = inset

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "inset": self.inset,
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [self.label],
        }


class DropdownMenuSeparator(Component):
    """A separator line in the dropdown menu."""

    component_type: str = "DropdownMenuSeparator"

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
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [],
        }


class DropdownMenuCheckboxItem(Component):
    """A checkbox item in the dropdown menu."""

    component_type: str = "DropdownMenuCheckboxItem"

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
            "className": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.on_checked_change:
            props["onCheckedChange"] = self.on_checked_change.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": [self.label],
        }


class DropdownMenuRadioGroup(Component):
    """A group of radio items in the dropdown menu."""

    component_type: str = "DropdownMenuRadioGroup"

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
            "className": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.on_value_change:
            props["onValueChange"] = self.on_value_change.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": self._render_children(),
        }


class DropdownMenuRadioItem(Component):
    """A radio item in the dropdown menu."""

    component_type: str = "DropdownMenuRadioItem"

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
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [self.label],
        }


class DropdownMenuSub(Component):
    """A submenu container."""

    component_type: str = "DropdownMenuSub"

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
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class DropdownMenuSubTrigger(Component):
    """A trigger for a submenu."""

    component_type: str = "DropdownMenuSubTrigger"

    def __init__(
        self,
        label: str,
        icon: str | None = None,
        inset: bool = False,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.label = label
        self.icon = icon
        self.inset = inset

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "icon": self.icon,
                "inset": self.inset,
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [self.label],
        }


class DropdownMenuSubContent(Component):
    """The content of a submenu."""

    component_type: str = "DropdownMenuSubContent"

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
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class ContextMenu(Component):
    """
    Displays a menu on right-click.

    Example:
        ```python
        ContextMenu(
            children=[
                ContextMenuTrigger(
                    Container("Right click here", class_name="border p-10")
                ),
                ContextMenuContent(
                    ContextMenuItem("Back"),
                    ContextMenuItem("Forward"),
                ),
            ]
        )
        ```
    """

    component_type: str = "ContextMenu"

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
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class ContextMenuTrigger(Component):
    """The element that triggers the context menu on right-click."""

    component_type: str = "ContextMenuTrigger"

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
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class ContextMenuContent(Component):
    """The content of the context menu."""

    component_type: str = "ContextMenuContent"

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
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class ContextMenuItem(Component):
    """A menu item in the context menu."""

    component_type: str = "ContextMenuItem"

    def __init__(
        self,
        label: str,
        icon: str | None = None,
        shortcut: str | None = None,
        disabled: bool = False,
        on_select: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.label = label
        self.icon = icon
        self.shortcut = shortcut
        self.disabled = disabled
        self.on_select = on_select

    def render(self) -> dict[str, Any]:
        props = {
            "icon": self.icon,
            "shortcut": self.shortcut,
            "disabled": self.disabled,
            "className": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.on_select:
            props["onSelect"] = self.on_select.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": [self.label],
        }


class ContextMenuSeparator(Component):
    """A separator in the context menu."""

    component_type: str = "ContextMenuSeparator"

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
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [],
        }


class ContextMenuCheckboxItem(Component):
    """A checkbox item in the context menu."""

    component_type: str = "ContextMenuCheckboxItem"

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
            "className": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.on_checked_change:
            props["onCheckedChange"] = self.on_checked_change.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": [self.label],
        }


class Drawer(Component):
    """
    A drawer component for mobile (using Vaul).

    Example:
        ```python
        Drawer(
            children=[
                DrawerTrigger(Button("Open Drawer")),
                DrawerContent(
                    DrawerHeader(
                        DrawerTitle("Move Goal"),
                        DrawerDescription("Set your daily goal."),
                    ),
                    DrawerFooter(Button("Submit")),
                ),
            ]
        )
        ```
    """

    component_type: str = "Drawer"

    def __init__(
        self,
        open: bool | None = None,
        on_open_change: Any = None,
        should_scale_background: bool = True,
        children: list["Component"] | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.open = open
        self.on_open_change = on_open_change
        self.should_scale_background = should_scale_background
        if children:
            self._children = children

    def render(self) -> dict[str, Any]:
        props = {
            "shouldScaleBackground": self.should_scale_background,
            "className": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.open is not None:
            props["open"] = self.open
        if self.on_open_change:
            props["onOpenChange"] = self.on_open_change.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": self._render_children(),
        }


class DrawerTrigger(Component):
    """The button that opens the drawer."""

    component_type: str = "DrawerTrigger"

    def __init__(
        self,
        children: Union[list["Component"], "Component", None] = None,
        as_child: bool = False,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.as_child = as_child
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
                "asChild": self.as_child,
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class DrawerContent(Component):
    """The content of the drawer."""

    component_type: str = "DrawerContent"

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
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class DrawerHeader(Component):
    """The header of the drawer."""

    component_type: str = "DrawerHeader"

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
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class DrawerFooter(Component):
    """The footer of the drawer."""

    component_type: str = "DrawerFooter"

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
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class DrawerTitle(Component):
    """The title of the drawer."""

    component_type: str = "DrawerTitle"

    def __init__(
        self,
        title: str,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.title = title

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [self.title],
        }


class DrawerDescription(Component):
    """The description of the drawer."""

    component_type: str = "DrawerDescription"

    def __init__(
        self,
        description: str,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.description = description

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [self.description],
        }


class DrawerClose(Component):
    """A button to close the drawer."""

    component_type: str = "DrawerClose"

    def __init__(
        self,
        children: Union[list["Component"], "Component", None] = None,
        as_child: bool = False,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.as_child = as_child
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
                "asChild": self.as_child,
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }
