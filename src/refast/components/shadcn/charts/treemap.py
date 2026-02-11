"""Treemap component."""

from typing import Any, Literal

from refast.components.base import Component
from refast.context import Callback


class Treemap(Component):
    """
    Treemap component for hierarchical data visualization.

    Example:
        ```python
        Treemap(
            data=data,
            data_key="size",
            aspect_ratio=4/3,
        )
        ```

    Args:
        data: Hierarchical data (can contain nested 'children')
        width: Width
        height: Height
        data_key: Key for values
        name_key: Key for names
        aspect_ratio: Aspect ratio for tiles
        type: Treemap type ("flat" or "nest")
        fill: Fill color
        stroke: Stroke color
        color_panel: List of colors for tiles
        is_animation_active: Enable animation
        animation_begin: Animation delay (ms)
        animation_duration: Animation duration (ms)
        animation_easing: Easing function
        on_click: Click event handler
        on_mouse_enter: Mouse enter handler
        on_mouse_leave: Mouse leave handler
    """

    component_type: str = "Treemap"

    def __init__(
        self,
        data: list[dict[str, Any]],
        width: int | str = "100%",
        height: int | str = 400,
        data_key: str = "value",
        name_key: str = "name",
        aspect_ratio: float = 1.0,
        type: Literal["flat", "nest"] = "flat",
        fill: str | None = None,
        stroke: str = "#fff",
        color_panel: list[str] | None = None,
        is_animation_active: bool | Literal["auto"] = "auto",
        animation_begin: int = 0,
        animation_duration: int = 1500,
        animation_easing: str = "ease",
        on_click: Callback | None = None,
        on_mouse_enter: Callback | None = None,
        on_mouse_leave: Callback | None = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.data = data
        self.width = width
        self.height = height
        self.data_key = data_key
        self.name_key = name_key
        self.aspect_ratio = aspect_ratio
        self.type = type
        self.fill = fill
        self.stroke = stroke
        self.color_panel = color_panel
        self.is_animation_active = is_animation_active
        self.animation_begin = animation_begin
        self.animation_duration = animation_duration
        self.animation_easing = animation_easing
        self.on_click = on_click
        self.on_mouse_enter = on_mouse_enter
        self.on_mouse_leave = on_mouse_leave
        self.extra_props = kwargs

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "data": self.data,
                "width": self.width,
                "height": self.height,
                "data_key": self.data_key,
                "name_key": self.name_key,
                "aspectRatio": self.aspect_ratio,
                "type": self.type,
                "fill": self.fill,
                "stroke": self.stroke,
                "colorPanel": self.color_panel,
                "isAnimationActive": self.is_animation_active,
                "animationBegin": self.animation_begin,
                "animation_duration": self.animation_duration,
                "animationEasing": self.animation_easing,
                "on_click": self.on_click.serialize() if self.on_click else None,
                "on_mouse_enter": (
                    self.on_mouse_enter.serialize() if self.on_mouse_enter else None
                ),
                "on_mouse_leave": (
                    self.on_mouse_leave.serialize() if self.on_mouse_leave else None
                ),
                **self.extra_props,
            },
        }
