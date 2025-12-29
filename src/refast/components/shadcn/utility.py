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
                "className": self.class_name,
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
                "className": self.class_name,
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
        children: Union[list["Component"], None] = None,
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
                "scrollHideDelay": self.scroll_hide_delay,
                "className": self.class_name,
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
                "className": self.class_name,
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
        children: Union[list["Component"], None] = None,
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
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "open": self.open,
                "defaultOpen": self.default_open,
                "onOpenChange": self.on_open_change.serialize() if self.on_open_change else None,
                "disabled": self.disabled,
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
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
                "asChild": self.as_child,
                "className": self.class_name,
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
                "className": self.class_name,
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
        children: Union[list["Component"], None] = None,
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
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class CarouselContent(Component):
    """The container for carousel items."""

    component_type: str = "CarouselContent"

    def __init__(
        self,
        children: Union[list["Component"], None] = None,
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
                "className": self.class_name,
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
                "className": self.class_name,
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
                "className": self.class_name,
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
        children: Union[list["Component"], None] = None,
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
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "direction": self.direction,
                "onLayout": self.on_layout.serialize() if self.on_layout else None,
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
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
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "defaultSize": self.default_size,
                "minSize": self.min_size,
                "maxSize": self.max_size,
                "collapsible": self.collapsible,
                "collapsedSize": self.collapsed_size,
                "onCollapse": self.on_collapse.serialize() if self.on_collapse else None,
                "onExpand": self.on_expand.serialize() if self.on_expand else None,
                "onResize": self.on_resize.serialize() if self.on_resize else None,
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
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
                "withHandle": self.with_handle,
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [],
        }


class Toaster(Component):
    """
    Toast notification container using Sonner.

    Example:
        ```python
        # In your layout
        Toaster(position="bottom-right")
        ```
    """

    component_type: str = "Toaster"

    def __init__(
        self,
        position: Literal[
            "top-left", "top-center", "top-right",
            "bottom-left", "bottom-center", "bottom-right"
        ] = "bottom-right",
        expand: bool = False,
        duration: int = 4000,
        visible_toasts: int = 3,
        close_button: bool = False,
        rich_colors: bool = False,
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

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "position": self.position,
                "expand": self.expand,
                "duration": self.duration,
                "visibleToasts": self.visible_toasts,
                "closeButton": self.close_button,
                "richColors": self.rich_colors,
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
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
                "className": self.class_name,
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
                "className": self.class_name,
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
                "className": self.class_name,
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
                "defaultTheme": self.default_theme,
                "storageKey": self.storage_key,
                "showSystemOption": self.show_system_option,
                "mode": self.mode,
                "onChange": self.on_change.serialize() if self.on_change else None,
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [],
        }

