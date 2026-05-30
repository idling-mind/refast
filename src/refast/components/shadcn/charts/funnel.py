"""Funnel chart components."""

from typing import Any, Literal

from refast.components.base import ChildrenType, Component
from refast.context import Callback


class FunnelChart(Component):
    """
    Funnel chart component.

    Example:
        ```python
        FunnelChart(
            Funnel(data=data, data_key="value", name_key="name"),
        )
        ```

    Args:
        margin: Chart margins
        on_click: Click event handler
        on_mouse_enter: Mouse enter handler
        on_mouse_leave: Mouse leave handler
    """

    component_type: str = "FunnelChart"

    def __init__(
        self,
        children: ChildrenType = None,
        margin: dict[str, int] | None = None,
        on_click: Callback | None = None,
        on_mouse_enter: Callback | None = None,
        on_mouse_leave: Callback | None = None,
        id: str | None = None,
        style: dict[str, Any] | None = None,
        parent_style: dict[str, Any] | None = None,
        extra_props: dict[str, Any] | None = None,
    ):
        super().__init__(id=id, extra_props=extra_props)
        self.margin = margin or {"top": 5, "right": 5, "left": 5, "bottom": 5}
        self.on_click = on_click
        self.on_mouse_enter = on_mouse_enter
        self.on_mouse_leave = on_mouse_leave

        self.add_children(children)

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "margin": self.margin,
                "on_click": self.on_click.serialize() if self.on_click else None,
                "on_mouse_enter": (
                    self.on_mouse_enter.serialize() if self.on_mouse_enter else None
                ),
                "on_mouse_leave": (
                    self.on_mouse_leave.serialize() if self.on_mouse_leave else None
                ),
            },
            "children": self._render_children(),
        }


class Funnel(Component):
    """
    Funnel component for FunnelChart.

    Args:
        data: Funnel data
        data_key: Key for values
        name_key: Key for names
        active_shape: Active shape configuration
        label: Label configuration
        legend_type: Legend icon type
        last_shape_type: Type of last shape ("triangle" or "rectangle")
        reversed: Reverse order
        is_animation_active: Enable animation
        animation_begin: Animation delay (ms)
        animation_duration: Animation duration (ms)
        animation_easing: Easing function
        hide: Hide the funnel
    """

    component_type: str = "Funnel"

    def __init__(
        self,
        data: list[dict[str, Any]],
        data_key: str,
        name_key: str | None = None,
        active_shape: dict[str, Any] | None = None,
        label: bool | dict[str, Any] | None = None,
        legend_type: str | None = None,
        last_shape_type: Literal["triangle", "rectangle"] = "triangle",
        reversed: bool = False,
        is_animation_active: bool | Literal["auto"] = "auto",
        animation_begin: int = 0,
        animation_duration: int = 1500,
        animation_easing: str = "ease",
        hide: bool = False,
        children: ChildrenType = None,
        id: str | None = None,
        style: dict[str, Any] | None = None,
        parent_style: dict[str, Any] | None = None,
        extra_props: dict[str, Any] | None = None,
    ):
        super().__init__(id=id, extra_props=extra_props)
        # Auto-inject fill colors by index when data items have no fill
        if data and not any("fill" in item for item in data):
            self.data = [
                {**item, "fill": f"hsl(var(--chart-{(i % 8) + 1}))"}
                for i, item in enumerate(data)
            ]
        else:
            self.data = list(data)
        self.data_key = data_key
        self.name_key = name_key
        self.active_shape = active_shape
        self.label = label
        self.legend_type = legend_type
        self.last_shape_type = last_shape_type
        self.reversed = reversed
        self.is_animation_active = is_animation_active
        self.animation_begin = animation_begin
        self.animation_duration = animation_duration
        self.animation_easing = animation_easing
        self.hide = hide

        self.add_children(children)

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "data": self.data,
                "data_key": self.data_key,
                "name_key": self.name_key,
                "activeShape": self.active_shape,
                "label": self.label,
                "legend_type": self.legend_type,
                "lastShapeType": self.last_shape_type,
                "reversed": self.reversed,
                "isAnimationActive": self.is_animation_active,
                "animationBegin": self.animation_begin,
                "animation_duration": self.animation_duration,
                "animationEasing": self.animation_easing,
                "hide": self.hide,
                **self.extra_props,
            },
            "children": self._render_children(),
        }
