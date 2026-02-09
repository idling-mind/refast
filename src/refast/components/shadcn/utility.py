"""Utility and advanced data display components based on shadcn/ui."""

from typing import Any, Literal, Union

from refast.components.base import Component


class Separator(Component):
    """
    A visual separator between content.

    Example:
        ```python
        Column(
            Heading("Title"),
            Separator(),
            Paragraph("Content below separator"),
        )
        ```
    """

    component_type: str = "Separator"

    def __init__(
        self,
        orientation: Literal["horizontal", "vertical"] = "horizontal",
        decorative: bool = True,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.orientation = orientation
        self.decorative = decorative

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "orientation": self.orientation,
                "decorative": self.decorative,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [],
        }


class AspectRatio(Component):
    """
    Displays content within a desired ratio.

    Example:
        ```python
        AspectRatio(
            ratio=16/9,
            children=[Image(src="...", alt="Photo")]
        )
        ```
    """

    component_type: str = "AspectRatio"

    def __init__(
        self,
        ratio: float = 1.0,
        children: Union[list["Component"], "Component", None] = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.ratio = ratio
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
                "ratio": self.ratio,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class ScrollArea(Component):
    """
    A scrollable area with custom scrollbars.

    Example:
        ```python
        ScrollArea(
            class_name="h-72 w-48",
            children=[
                # Long content here
            ]
        )
        ```
    """

    component_type: str = "ScrollArea"

    def __init__(
        self,
        children: list["Component"] | None = None,
        type: Literal["auto", "always", "scroll", "hover"] = "hover",
        scroll_hide_delay: int = 600,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.scroll_type = type
        self.scroll_hide_delay = scroll_hide_delay
        if children:
            self._children = children

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "type": self.scroll_type,
                "scroll_hide_delay": self.scroll_hide_delay,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class ScrollBar(Component):
    """A scrollbar for ScrollArea."""

    component_type: str = "ScrollBar"

    def __init__(
        self,
        orientation: Literal["horizontal", "vertical"] = "vertical",
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
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [],
        }


class Collapsible(Component):
    """
    A component that expands/collapses content.

    Example:
        ```python
        Collapsible(
            children=[
                CollapsibleTrigger(Button("Toggle")),
                CollapsibleContent(
                    Paragraph("This content can be collapsed."),
                ),
            ]
        )
        ```
    """

    component_type: str = "Collapsible"

    def __init__(
        self,
        open: bool | None = None,
        default_open: bool = False,
        on_open_change: Any = None,
        disabled: bool = False,
        children: list["Component"] | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.open = open
        self.default_open = default_open
        self.on_open_change = on_open_change
        self.disabled = disabled
        if children:
            self._children = children

    def render(self) -> dict[str, Any]:
        props = {
            "default_open": self.default_open,
            "disabled": self.disabled,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.open is not None:
            props["open"] = self.open
        if self.on_open_change:
            props["on_open_change"] = self.on_open_change.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": self._render_children(),
        }


class CollapsibleTrigger(Component):
    """The button that toggles the collapsible."""

    component_type: str = "CollapsibleTrigger"

    def __init__(
        self,
        children: Union[list["Component"], "Component", None] = None,
        as_child: bool = True,
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
                "as_child": self.as_child,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class CollapsibleContent(Component):
    """The content that can be collapsed."""

    component_type: str = "CollapsibleContent"

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


class Carousel(Component):
    """
    A carousel with motion and swipe gestures.

    Example:
        ```python
        Carousel(
            children=[
                CarouselContent(
                    CarouselItem(Card(...)),
                    CarouselItem(Card(...)),
                ),
                CarouselPrevious(),
                CarouselNext(),
            ]
        )
        ```
    """

    component_type: str = "Carousel"

    def __init__(
        self,
        children: list["Component"] | None = None,
        orientation: Literal["horizontal", "vertical"] = "horizontal",
        opts: dict[str, Any] | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.orientation = orientation
        self.opts = opts or {}
        if children:
            self._children = children

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "orientation": self.orientation,
                "opts": self.opts,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class CarouselContent(Component):
    """The container for carousel items."""

    component_type: str = "CarouselContent"

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


class CarouselItem(Component):
    """A single item in the carousel."""

    component_type: str = "CarouselItem"

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


class CarouselPrevious(Component):
    """The previous button for the carousel."""

    component_type: str = "CarouselPrevious"

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


class CarouselNext(Component):
    """The next button for the carousel."""

    component_type: str = "CarouselNext"

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


class ResizablePanelGroup(Component):
    """
    A resizable panel group.

    Example:
        ```python
        ResizablePanelGroup(
            direction="horizontal",
            children=[
                ResizablePanel(default_size=50, children=[Paragraph("One")]),
                ResizableHandle(),
                ResizablePanel(default_size=50, children=[Paragraph("Two")]),
            ]
        )
        ```
    """

    component_type: str = "ResizablePanelGroup"

    def __init__(
        self,
        direction: Literal["horizontal", "vertical"] = "horizontal",
        children: list["Component"] | None = None,
        on_layout: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.direction = direction
        self.on_layout = on_layout
        if children:
            self._children = children

    def render(self) -> dict[str, Any]:
        props = {
            "direction": self.direction,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.on_layout:
            props["on_layout"] = self.on_layout.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": self._render_children(),
        }


class ResizablePanel(Component):
    """A resizable panel."""

    component_type: str = "ResizablePanel"

    def __init__(
        self,
        default_size: float = 50,
        min_size: float | None = None,
        max_size: float | None = None,
        collapsible: bool = False,
        collapsed_size: float | None = None,
        on_collapse: Any = None,
        on_expand: Any = None,
        on_resize: Any = None,
        children: Union[list["Component"], "Component", None] = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.default_size = default_size
        self.min_size = min_size
        self.max_size = max_size
        self.collapsible = collapsible
        self.collapsed_size = collapsed_size
        self.on_collapse = on_collapse
        self.on_expand = on_expand
        self.on_resize = on_resize
        if children:
            if isinstance(children, list):
                self._children = children
            else:
                self._children = [children]

    def render(self) -> dict[str, Any]:
        props = {
            "default_size": self.default_size,
            "min_size": self.min_size,
            "max_size": self.max_size,
            "collapsible": self.collapsible,
            "collapsed_size": self.collapsed_size,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.on_collapse:
            props["on_collapse"] = self.on_collapse.serialize()
        if self.on_expand:
            props["on_expand"] = self.on_expand.serialize()
        if self.on_resize:
            props["on_resize"] = self.on_resize.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": self._render_children(),
        }


class ResizableHandle(Component):
    """A handle between resizable panels."""

    component_type: str = "ResizableHandle"

    def __init__(
        self,
        with_handle: bool = False,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.with_handle = with_handle

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "with_handle": self.with_handle,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [],
        }


class Toaster(Component):
    """
    Toast notification container using Sonner.

    This component renders the Sonner Toaster which displays all toast notifications.
    Place this component once in your layout (typically at the root).

    Args:
        position: Where toasts appear - "top-left", "top-center", "top-right",
                 "bottom-left", "bottom-center", "bottom-right"
        expand: Whether toasts are expanded by default on hover
        duration: Default duration in ms for all toasts (default: 4000)
        visible_toasts: Maximum number of visible toasts at once (default: 3)
        close_button: Whether to show close button on toasts
        rich_colors: Whether to use rich colors for variants
        theme: Color theme - "light", "dark", or "system"
        offset: Offset from the edge of the screen (px or CSS value)
        gap: Gap between toasts in pixels (default: 14)
        dir: Text direction - "ltr", "rtl", or "auto"
        hotkey: Keyboard shortcut to focus toasts (default: Alt+T)
        invert: Whether to invert default colors

    Example:
        ```python
        # Basic usage in layout
        Container(
            children=[
                # Your app content
                Toaster(position="bottom-right", rich_colors=True)
            ]
        )

        # Customized toaster
        Toaster(
            position="top-center",
            expand=True,
            visible_toasts=5,
            close_button=True,
            theme="dark"
        )
        ```
    """

    component_type: str = "Toaster"

    def __init__(
        self,
        position: Literal[
            "top-left", "top-center", "top-right", "bottom-left", "bottom-center", "bottom-right"
        ] = "bottom-right",
        expand: bool = False,
        duration: int = 4000,
        visible_toasts: int = 3,
        close_button: bool = False,
        rich_colors: bool = False,
        theme: Literal["light", "dark", "system"] = "system",
        offset: str | int | None = None,
        gap: int = 14,
        dir: Literal["ltr", "rtl", "auto"] = "auto",
        hotkey: list[str] | None = None,
        invert: bool = False,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.position = position
        self.expand = expand
        self.duration = duration
        self.visible_toasts = visible_toasts
        self.close_button = close_button
        self.rich_colors = rich_colors
        self.theme = theme
        self.offset = offset
        self.gap = gap
        self.dir = dir
        self.hotkey = hotkey or ["altKey", "KeyT"]
        self.invert = invert

    def render(self) -> dict[str, Any]:
        props: dict[str, Any] = {
            "position": self.position,
            "expand": self.expand,
            "duration": self.duration,
            "visible_toasts": self.visible_toasts,
            "close_button": self.close_button,
            "rich_colors": self.rich_colors,
            "theme": self.theme,
            "gap": self.gap,
            "dir": self.dir,
            "hotkey": self.hotkey,
            "invert": self.invert,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        # Only include offset if set
        if self.offset is not None:
            props["offset"] = self.offset

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": [],
        }


class Empty(Component):
    """
    An empty state component.

    Example:
        ```python
        Empty(
            icon="Inbox",
            title="No messages",
            description="You don't have any messages yet.",
            action=Button("Send a message"),
        )
        ```
    """

    component_type: str = "Empty"

    def __init__(
        self,
        icon: str | None = None,
        title: str = "",
        description: str = "",
        action: "Component | None" = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.icon = icon
        self.title = title
        self.description = description
        self.action = action

    def render(self) -> dict[str, Any]:
        children = []
        if self.action:
            children.append(self.action.render())
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "icon": self.icon,
                "title": self.title,
                "description": self.description,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": children,
        }


class Kbd(Component):
    """
    Keyboard key display.

    Example:
        ```python
        Paragraph("Press ", Kbd("⌘"), " + ", Kbd("K"), " to open command menu.")
        ```
    """

    component_type: str = "Kbd"

    def __init__(
        self,
        key: str,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.key = key

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [self.key],
        }


class LoadingOverlay(Component):
    """
    Global loading state overlay.

    Example:
        ```python
        LoadingOverlay(
            loading=ctx.state.is_loading,
            text="Loading...",
        )
        ```
    """

    component_type: str = "LoadingOverlay"

    def __init__(
        self,
        loading: bool = False,
        text: str = "Loading...",
        blur: bool = True,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.loading = loading
        self.text = text
        self.blur = blur

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "loading": self.loading,
                "text": self.text,
                "blur": self.blur,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [],
        }


class ThemeSwitcher(Component):
    """
    Theme switcher component for toggling between light and dark themes.

    This component provides a button to switch between light and dark themes.
    It supports system theme detection and persistence via localStorage.

    Example:
        ```python
        # Basic usage with default themes
        ThemeSwitcher()

        # With specific default theme
        ThemeSwitcher(default_theme="dark")

        # With callback for theme changes
        ThemeSwitcher(
            on_change=ctx.callback(handle_theme_change),
        )

        # With custom storage key
        ThemeSwitcher(storage_key="my-app-theme")
        ```

    Args:
        default_theme: Default theme to use if no preference is stored.
            One of "light", "dark", or "system". Defaults to "system".
        storage_key: LocalStorage key for persisting theme preference.
            Defaults to "refast-theme".
        show_system_option: Whether to show the system option in dropdown mode.
            Defaults to True.
        mode: Display mode - "toggle" for simple switch, "dropdown" for menu.
            Defaults to "toggle".
        on_change: Callback fired when theme changes. Receives the new theme value.
    """

    component_type: str = "ThemeSwitcher"

    def __init__(
        self,
        default_theme: Literal["light", "dark", "system"] = "system",
        storage_key: str = "refast-theme",
        show_system_option: bool = True,
        mode: Literal["toggle", "dropdown"] = "toggle",
        on_change: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.default_theme = default_theme
        self.storage_key = storage_key
        self.show_system_option = show_system_option
        self.mode = mode
        self.on_change = on_change

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "default_theme": self.default_theme,
                "storage_key": self.storage_key,
                "show_system_option": self.show_system_option,
                "mode": self.mode,
                "on_change": self.on_change.serialize() if self.on_change else None,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [],
        }
