"""Icon component using Lucide icons."""

from typing import Any, Literal

from refast.components.base import Component


class Icon(Component):
    """
    Icon component that renders Lucide icons by name.

    The Icon component provides access to a curated set of ~100 commonly-used
    Lucide icons. Icons can be used standalone or as children of other components.

    Example:
        ```python
        # Standalone icon
        Icon("home", size=24, color="blue")

        # As child of other component
        Button("Save", children=[Icon("save")])

        # With sidebar
        SidebarMenuButton("Dashboard", icon="home")
        ```

    Available icons include:
    - Navigation: home, menu, chevron-left, chevron-right, chevron-up, chevron-down,
                  arrow-left, arrow-right, arrow-up, arrow-down
    - Actions: plus, minus, x, check, edit, trash, save, copy, paste, cut, undo, redo
    - Files: file, folder, upload, download, image, video, music, archive
    - UI: search, settings, filter, sort, more-horizontal, more-vertical, grip-vertical
    - Users: user, users, user-plus, user-minus, log-in, log-out
    - Status: check-circle, x-circle, alert-circle, info, alert-triangle, loader
    - Communication: mail, send, message-circle, bell, phone
    - And many more...

    For backward compatibility, if an icon name is not found in the Lucide icon set,
    it will be rendered as plain text (supporting emojis like "🏠").

    Args:
        name: The Lucide icon name (e.g., "home", "settings", "user") or fallback text/emoji
        size: Icon size in pixels (default: 16)
        color: Icon color (CSS color value, e.g., "red", "#ff0000", "currentColor")
        stroke_width: Stroke width for the icon (default: 2)
        class_name: Additional CSS classes
    """

    component_type: str = "Icon"

    def __init__(
        self,
        name: str,
        size: int = 16,
        color: str | None = None,
        stroke_width: float = 2,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.name = name
        self.size = size
        self.color = color
        self.stroke_width = stroke_width

    def render(self) -> dict[str, Any]:
        props = {
            "name": self.name,
            "size": self.size,
            "stroke_width": self.stroke_width,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.color:
            props["color"] = self.color

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": [],
        }


# Common icon names for documentation and IDE completion
ICON_NAMES = Literal[
    # Navigation
    "home",
    "menu",
    "chevron-left",
    "chevron-right",
    "chevron-up",
    "chevron-down",
    "chevrons-left",
    "chevrons-right",
    "chevrons-up",
    "chevrons-down",
    "arrow-left",
    "arrow-right",
    "arrow-up",
    "arrow-down",
    "arrow-up-right",
    "arrow-down-left",
    "corner-up-left",
    "corner-up-right",
    "move",
    "external-link",
    # Actions
    "plus",
    "minus",
    "x",
    "check",
    "edit",
    "edit-2",
    "edit-3",
    "trash",
    "trash-2",
    "save",
    "copy",
    "clipboard",
    "clipboard-check",
    "paste",
    "cut",
    "undo",
    "redo",
    "refresh-cw",
    "rotate-ccw",
    "rotate-cw",
    # Files
    "file",
    "file-text",
    "file-plus",
    "file-minus",
    "file-check",
    "file-x",
    "folder",
    "folder-open",
    "folder-plus",
    "folder-minus",
    "upload",
    "download",
    "cloud-off",
    "image",
    "video",
    "music",
    "archive",
    # UI
    "search",
    "settings",
    "settings-2",
    "sliders",
    "filter",
    "sort-asc",
    "sort-desc",
    "more-horizontal",
    "more-vertical",
    "grip-vertical",
    "grip-horizontal",
    "maximize",
    "minimize",
    "maximize-2",
    "minimize-2",
    "expand",
    "shrink",
    "eye",
    "eye-off",
    "lock",
    "unlock",
    "key",
    "link",
    "link-2",
    "unlink",
    # Users
    "user",
    "users",
    "user-plus",
    "user-minus",
    "user-check",
    "user-x",
    "log-in",
    "log-out",
    # Status
    "check-circle",
    "check-circle-2",
    "x-circle",
    "alert-circle",
    "info",
    "alert-triangle",
    "loader",
    "loader-2",
    "circle",
    "circle-dot",
    "ban",
    # Communication
    "mail",
    "mail-open",
    "send",
    "inbox",
    "message-circle",
    "message-square",
    "bell",
    "bell-off",
    "phone",
    "phone-call",
    "phone-off",
    # Media
    "play",
    "pause",
    "stop-circle",
    "skip-back",
    "skip-forward",
    "fast-forward",
    "rewind",
    "volume",
    "volume-1",
    "volume-2",
    "volume-x",
    # Data
    "bar-chart",
    "bar-chart-2",
    "line-chart",
    "pie-chart",
    "activity",
    "trending-up",
    "trending-down",
    "database",
    "server",
    # Layout
    "layout",
    "layout-grid",
    "layout-list",
    "sidebar",
    "panel-left",
    "panel-right",
    "panel-top",
    "panel-bottom",
    "columns",
    "rows",
    # Misc
    "star",
    "heart",
    "thumbs-up",
    "thumbs-down",
    "bookmark",
    "flag",
    "tag",
    "hash",
    "at-sign",
    "calendar",
    "clock",
    "timer",
    "alarm-clock",
    "map",
    "map-pin",
    "navigation",
    "compass",
    "globe",
    "wifi",
    "wifi-off",
    "bluetooth",
    "battery",
    "power",
    "zap",
    "sun",
    "moon",
    "cloud",
    "umbrella",
    "thermometer",
    "droplet",
    "wind",
    "code",
    "terminal",
    "github",
    "gitlab",
    "package",
    "box",
    "shopping-cart",
    "shopping-bag",
    "credit-card",
    "dollar-sign",
    "percent",
    "gift",
    "truck",
    "printer",
    "camera",
    "mic",
    "headphones",
    "monitor",
    "smartphone",
    "tablet",
    "laptop",
    "watch",
    "tv",
    "cpu",
    "hard-drive",
    "shield",
    "shield-check",
    "award",
    "target",
    "crosshair",
    "layers",
    "square",
    "circle",
    "triangle",
    "hexagon",
    "octagon",
    "help-circle",
    "life-buoy",
    # Additional icons
    "rocket",
    "grid-3x3",
    "mouse-pointer-click",
    "route",
    "radio",
    "palette",
    "component",
    "type",
    "text-cursor-input",
    "table",
    "bar-chart-3",
    "wrench",
    "hammer",
    "puzzle",
    "paintbrush",
    "hand-metal",
    "check-square",
    "layout-dashboard",
]
