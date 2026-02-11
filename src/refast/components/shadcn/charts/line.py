"""Line chart components."""

from typing import Any, Literal

from refast.components.base import Component
from refast.context import Callback


class LineChart(Component):
    """
    Line chart component.

    Example:
        ```python
        LineChart(
            data=data,
            Line(data_key="items", stroke="hsl(var(--chart-1))"),
        )
        ```

    Args:
        data: List of data dictionaries
        margin: Chart margins
        layout: Chart layout direction
        sync_id: ID for syncing multiple charts
        sync_method: How to sync charts
        on_click: Click event handler
        on_mouse_enter: Mouse enter handler
        on_mouse_leave: Mouse leave handler
        on_mouse_move: Mouse move handler
    """

    component_type: str = "LineChart"

    def __init__(
        self,
        *children: Component,
        data: list[dict[str, Any]],
        margin: dict[str, int] | None = None,
        layout: Literal["horizontal", "vertical"] = "horizontal",
        sync_id: str | None = None,
        sync_method: Literal["index", "value"] | None = None,
        on_click: Callback | None = None,
        on_mouse_enter: Callback | None = None,
        on_mouse_leave: Callback | None = None,
        on_mouse_move: Callback | None = None,
        **kwargs: Any,
    ):
        kw_children = kwargs.pop("children", None)
        super().__init__(**kwargs)
        self.data = data
        self.margin = margin or {"top": 10, "right": 10, "left": 10, "bottom": 0}
        self.layout = layout
        self.sync_id = sync_id
        self.sync_method = sync_method
        self.on_click = on_click
        self.on_mouse_enter = on_mouse_enter
        self.on_mouse_leave = on_mouse_leave
        self.on_mouse_move = on_mouse_move

        self.children = list(children)
        if kw_children:
            if isinstance(kw_children, list):
                self.children.extend(kw_children)
            else:
                self.children.append(kw_children)

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "data": self.data,
                "margin": self.margin,
                "layout": self.layout,
                "syncId": self.sync_id,
                "syncMethod": self.sync_method,
                "on_click": self.on_click.serialize() if self.on_click else None,
                "on_mouse_enter": (
                    self.on_mouse_enter.serialize() if self.on_mouse_enter else None
                ),
                "on_mouse_leave": (
                    self.on_mouse_leave.serialize() if self.on_mouse_leave else None
                ),
                "on_mouse_move": (self.on_mouse_move.serialize() if self.on_mouse_move else None),
            },
            "children": [c.render() for c in self.children],
        }


class Line(Component):
    """
    Line component for LineChart.

    Args:
        data_key: Key from data
        type: Interpolation type
        stroke: Stroke color
        stroke_width: Stroke width
        dot: Whether to show dots
        active_dot: Active dot configuration
        connect_nulls: Connect across null points
        x_axis_id: XAxis reference
        y_axis_id: YAxis reference
        legend_type: Legend icon type
        name: Name for tooltip/legend
        unit: Unit for tooltip
        label: Label configuration
        stroke_dasharray: Dash pattern
        is_animation_active: Enable animation
        animation_begin: Animation delay (ms)
        animation_duration: Animation duration (ms)
        animation_easing: Easing function
        hide: Hide the line
    """

    component_type: str = "Line"

    def __init__(
        self,
        data_key: str,
        type: Literal[
            "basis", "linear", "natural", "monotone", "step", "stepBefore", "stepAfter"
        ] = "natural",
        stroke: str = "hsl(var(--chart-1))",
        stroke_width: int = 2,
        dot: bool | dict[str, Any] = True,
        active_dot: bool | dict[str, Any] = True,
        connect_nulls: bool = False,
        x_axis_id: str | int | None = None,
        y_axis_id: str | int | None = None,
        legend_type: str | None = None,
        name: str | None = None,
        unit: str | None = None,
        label: bool | dict[str, Any] | None = None,
        stroke_dasharray: str | None = None,
        is_animation_active: bool | Literal["auto"] = "auto",
        animation_begin: int = 0,
        animation_duration: int = 1500,
        animation_easing: str = "ease",
        hide: bool = False,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.data_key = data_key
        self.type = type
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.dot = dot
        self.active_dot = active_dot
        self.connect_nulls = connect_nulls
        self.x_axis_id = x_axis_id
        self.y_axis_id = y_axis_id
        self.legend_type = legend_type
        self.name = name
        self.unit = unit
        self.label = label
        self.stroke_dasharray = stroke_dasharray
        self.is_animation_active = is_animation_active
        self.animation_begin = animation_begin
        self.animation_duration = animation_duration
        self.animation_easing = animation_easing
        self.hide = hide
        self.extra_props = kwargs

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "data_key": self.data_key,
                "type": self.type,
                "stroke": self.stroke,
                "stroke_width": self.stroke_width,
                "dot": self.dot,
                "activeDot": self.active_dot,
                "connectNulls": self.connect_nulls,
                "x_axis_id": self.x_axis_id,
                "y_axis_id": self.y_axis_id,
                "legend_type": self.legend_type,
                "name": self.name,
                "unit": self.unit,
                "label": self.label,
                "stroke_dasharray": self.stroke_dasharray,
                "isAnimationActive": self.is_animation_active,
                "animationBegin": self.animation_begin,
                "animation_duration": self.animation_duration,
                "animationEasing": self.animation_easing,
                "hide": self.hide,
                **self.extra_props,
            },
        }
