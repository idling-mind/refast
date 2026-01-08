"""Area chart components."""

from typing import Any, Literal

from refast.components.base import Component
from refast.events.types import Callback


class AreaChart(Component):
    """
    Area chart component.

    Example:
        ```python
        AreaChart(
            data=data,
            margin={"top": 10, "right": 10, "left": 10, "bottom": 0},
            layout="horizontal",
            Area(data_key="value", fill="hsl(var(--chart-1))"),
        )
        ```

    Args:
        data: List of data dictionaries
        margin: Chart margins
        stack_offset: Stack offset type for stacked areas
        layout: Chart layout direction
        sync_id: ID for syncing multiple charts
        sync_method: How to sync charts
        base_value: Base value for area
        on_click: Click event handler
        on_mouse_enter: Mouse enter handler
        on_mouse_leave: Mouse leave handler
        on_mouse_move: Mouse move handler
    """

    component_type: str = "AreaChart"

    def __init__(
        self,
        *children: Component,
        data: list[dict[str, Any]],
        margin: dict[str, int] | None = None,
        stack_offset: Literal["expand", "none", "wiggle", "silhouette"] | None = None,
        layout: Literal["horizontal", "vertical"] = "horizontal",
        sync_id: str | None = None,
        sync_method: Literal["index", "value"] | None = None,
        base_value: int | Literal["dataMin", "dataMax", "auto"] | None = None,
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
        self.stack_offset = stack_offset
        self.layout = layout
        self.sync_id = sync_id
        self.sync_method = sync_method
        self.base_value = base_value
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
                "stackOffset": self.stack_offset,
                "layout": self.layout,
                "syncId": self.sync_id,
                "syncMethod": self.sync_method,
                "baseValue": self.base_value,
                "onClick": self.on_click.serialize() if self.on_click else None,
                "onMouseEnter": (self.on_mouse_enter.serialize() if self.on_mouse_enter else None),
                "onMouseLeave": (self.on_mouse_leave.serialize() if self.on_mouse_leave else None),
                "onMouseMove": (self.on_mouse_move.serialize() if self.on_mouse_move else None),
            },
            "children": [c.render() for c in self.children],
        }


class Area(Component):
    """
    Area component for AreaChart.

    Args:
        data_key: Key from data to use for values
        type: Interpolation type
        fill: Fill color
        fill_opacity: Fill opacity (0-1)
        stroke: Stroke color
        stroke_width: Stroke width
        stacked_id: ID for stacking multiple areas
        base_value: Baseline value
        connect_nulls: Connect across null points
        dot: Dot configuration
        active_dot: Active dot config
        label: Label configuration
        legend_type: Legend icon type
        name: Name for tooltip/legend
        unit: Unit for tooltip
        x_axis_id: XAxis reference
        y_axis_id: YAxis reference
        is_animation_active: Enable animation
        animation_begin: Animation delay (ms)
        animation_duration: Animation duration (ms)
        animation_easing: Easing function
        hide: Hide the area
    """

    component_type: str = "Area"

    def __init__(
        self,
        data_key: str,
        type: Literal[
            "basis", "linear", "natural", "monotone", "step", "stepBefore", "stepAfter"
        ] = "natural",
        fill: str = "hsl(var(--chart-1))",
        fill_opacity: float = 0.4,
        stroke: str | None = None,
        stroke_width: int = 2,
        stacked_id: str | None = None,
        base_value: int | Literal["dataMin", "dataMax"] | None = None,
        connect_nulls: bool = False,
        dot: bool | dict[str, Any] = False,
        active_dot: bool | dict[str, Any] = True,
        label: bool | dict[str, Any] | None = None,
        legend_type: str | None = None,
        name: str | None = None,
        unit: str | None = None,
        x_axis_id: str | int | None = None,
        y_axis_id: str | int | None = None,
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
        self.fill = fill
        self.fill_opacity = fill_opacity
        self.stroke = stroke or fill
        self.stroke_width = stroke_width
        self.stacked_id = stacked_id
        self.base_value = base_value
        self.connect_nulls = connect_nulls
        self.dot = dot
        self.active_dot = active_dot
        self.label = label
        self.legend_type = legend_type
        self.name = name
        self.unit = unit
        self.x_axis_id = x_axis_id
        self.y_axis_id = y_axis_id
        self.is_animation_active = is_animation_active
        self.animation_begin = animation_begin
        self.animation_duration = animation_duration
        self.animation_easing = animation_easing
        self.hide = hide

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "dataKey": self.data_key,
                "type": self.type,
                "fill": self.fill,
                "fillOpacity": self.fill_opacity,
                "stroke": self.stroke,
                "strokeWidth": self.stroke_width,
                "stackId": self.stacked_id,
                "baseValue": self.base_value,
                "connectNulls": self.connect_nulls,
                "dot": self.dot,
                "activeDot": self.active_dot,
                "label": self.label,
                "legendType": self.legend_type,
                "name": self.name,
                "unit": self.unit,
                "xAxisId": self.x_axis_id,
                "yAxisId": self.y_axis_id,
                "isAnimationActive": self.is_animation_active,
                "animationBegin": self.animation_begin,
                "animationDuration": self.animation_duration,
                "animationEasing": self.animation_easing,
                "hide": self.hide,
            },
        }
