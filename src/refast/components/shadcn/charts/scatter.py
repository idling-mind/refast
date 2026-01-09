"""Scatter chart components."""

from typing import Any, Literal

from refast.components.base import Component
from refast.events.types import Callback


class ScatterChart(Component):
    """
    Scatter chart component for 2D/3D scatter plots.

    Example:
        ```python
        ScatterChart(
            data=data,
            Scatter(data_key="value", fill="hsl(var(--chart-1))"),
            XAxis(data_key="x", type="number"),
            YAxis(data_key="y", type="number"),
        )
        ```

    Args:
        data: List of data dictionaries (optional, can be set on Scatter)
        margin: Chart margins
        layout: Chart layout direction
        sync_id: ID for syncing multiple charts
        sync_method: How to sync charts
        on_click: Click event handler
        on_mouse_enter: Mouse enter handler
        on_mouse_leave: Mouse leave handler
        on_mouse_move: Mouse move handler
    """

    component_type: str = "ScatterChart"

    def __init__(
        self,
        *children: Component,
        data: list[dict[str, Any]] | None = None,
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
        self.margin = margin or {"top": 20, "right": 20, "left": 20, "bottom": 20}
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
                "on_mouse_enter": (self.on_mouse_enter.serialize() if self.on_mouse_enter else None),
                "on_mouse_leave": (self.on_mouse_leave.serialize() if self.on_mouse_leave else None),
                "on_mouse_move": (self.on_mouse_move.serialize() if self.on_mouse_move else None),
            },
            "children": [c.render() for c in self.children],
        }


class Scatter(Component):
    """
    Scatter component for ScatterChart.

    Args:
        data: Scatter data points
        data_key: Data key for values
        x_axis_id: XAxis reference
        y_axis_id: YAxis reference
        z_axis_id: ZAxis reference (for size)
        line: Connecting line configuration
        line_type: Line type
        line_joint_type: Line curve type
        shape: Point shape ("circle", "cross", "diamond", "square", "star",
               "triangle", "wye")
        active_shape: Active shape configuration
        legend_type: Legend icon type
        name: Name for tooltip/legend
        fill: Fill color
        label: Label configuration
        is_animation_active: Enable animation
        animation_begin: Animation delay (ms)
        animation_duration: Animation duration (ms)
        animation_easing: Easing function
        hide: Hide the scatter
    """

    component_type: str = "Scatter"

    def __init__(
        self,
        data: list[dict[str, Any]] | None = None,
        data_key: str | None = None,
        x_axis_id: str | int | None = None,
        y_axis_id: str | int | None = None,
        z_axis_id: str | int | None = None,
        line: bool | dict[str, Any] = False,
        line_type: Literal["joint", "fitting"] = "joint",
        line_joint_type: str = "linear",
        shape: str = "circle",
        active_shape: dict[str, Any] | None = None,
        legend_type: str | None = None,
        name: str | None = None,
        fill: str = "hsl(var(--chart-1))",
        label: bool | dict[str, Any] | None = None,
        is_animation_active: bool | Literal["auto"] = "auto",
        animation_begin: int = 0,
        animation_duration: int = 1500,
        animation_easing: str = "ease",
        hide: bool = False,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.data = data
        self.data_key = data_key
        self.x_axis_id = x_axis_id
        self.y_axis_id = y_axis_id
        self.z_axis_id = z_axis_id
        self.line = line
        self.line_type = line_type
        self.line_joint_type = line_joint_type
        self.shape = shape
        self.active_shape = active_shape
        self.legend_type = legend_type
        self.name = name
        self.fill = fill
        self.label = label
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
                "data": self.data,
                "data_key": self.data_key,
                "x_axis_id": self.x_axis_id,
                "y_axis_id": self.y_axis_id,
                "zAxisId": self.z_axis_id,
                "line": self.line,
                "lineType": self.line_type,
                "lineJointType": self.line_joint_type,
                "shape": self.shape,
                "activeShape": self.active_shape,
                "legend_type": self.legend_type,
                "name": self.name,
                "fill": self.fill,
                "label": self.label,
                "isAnimationActive": self.is_animation_active,
                "animationBegin": self.animation_begin,
                "animation_duration": self.animation_duration,
                "animationEasing": self.animation_easing,
                "hide": self.hide,
                **self.extra_props,
            },
        }


class ZAxis(Component):
    """
    Z-axis component for ScatterChart (controls point size).

    Args:
        z_axis_id: Unique axis ID
        data_key: Data key for Z values
        type: Axis type
        name: Axis name
        unit: Unit string
        range: Size range [min, max]
        scale: Scale type
        domain: Domain values
    """

    component_type: str = "ZAxis"

    def __init__(
        self,
        z_axis_id: str | int | None = None,
        data_key: str | None = None,
        type: Literal["number", "category"] = "number",
        name: str | None = None,
        unit: str | None = None,
        range: list[int] | None = None,
        scale: str = "auto",
        domain: list[Any] | None = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.z_axis_id = z_axis_id
        self.data_key = data_key
        self.type = type
        self.name = name
        self.unit = unit
        self.range = range or [60, 400]
        self.scale = scale
        self.domain = domain
        self.extra_props = kwargs

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "zAxisId": self.z_axis_id,
                "data_key": self.data_key,
                "type": self.type,
                "name": self.name,
                "unit": self.unit,
                "range": self.range,
                "scale": self.scale,
                "domain": self.domain,
                **self.extra_props,
            },
        }


