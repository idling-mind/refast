"""Pie chart components."""

from typing import Any, Literal

from refast.components.base import Component
from refast.events.types import Callback


class PieChart(Component):
    """
    Pie chart component.

    Example:
        ```python
        PieChart(
            Pie(data=data, data_key="value", name_key="name"),
        )
        ```

    Args:
        margin: Chart margins
        on_click: Click event handler
        on_mouse_enter: Mouse enter handler
        on_mouse_leave: Mouse leave handler
    """

    component_type: str = "PieChart"

    def __init__(
        self,
        *children: Component,
        margin: dict[str, int] | None = None,
        on_click: Callback | None = None,
        on_mouse_enter: Callback | None = None,
        on_mouse_leave: Callback | None = None,
        **kwargs: Any,
    ):
        kw_children = kwargs.pop("children", None)
        super().__init__(**kwargs)
        self.margin = margin or {"top": 0, "right": 0, "left": 0, "bottom": 0}
        self.on_click = on_click
        self.on_mouse_enter = on_mouse_enter
        self.on_mouse_leave = on_mouse_leave

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
                "margin": self.margin,
                "on_click": self.on_click.serialize() if self.on_click else None,
                "on_mouse_enter": (self.on_mouse_enter.serialize() if self.on_mouse_enter else None),
                "on_mouse_leave": (self.on_mouse_leave.serialize() if self.on_mouse_leave else None),
            },
            "children": [c.render() for c in self.children],
        }


class Pie(Component):
    """
    Pie component for PieChart.

    Args:
        data: List of data dictionaries
        data_key: Key for values
        name_key: Key for names
        cx: X center (percentage string or pixel value)
        cy: Y center (percentage string or pixel value)
        inner_radius: Inner radius (for donuts)
        outer_radius: Outer radius
        label: Label configuration
        start_angle: Start angle (degrees)
        end_angle: End angle (degrees)
        padding_angle: Padding between sectors
        corner_radius: Corner radius
        min_angle: Minimum sector angle
        label_line: Label line config
        legend_type: Legend icon type
        active_shape: Active sector styling
        inactive_shape: Inactive sector styling
        is_animation_active: Enable animation
        animation_begin: Animation delay (ms)
        animation_duration: Animation duration (ms)
        animation_easing: Easing function
        hide: Hide the pie
    """

    component_type: str = "Pie"

    def __init__(
        self,
        *children: Component,
        data: list[dict[str, Any]],
        data_key: str,
        name_key: str,
        cx: str | int = "50%",
        cy: str | int = "50%",
        inner_radius: int | str = 0,
        outer_radius: int | str = "80%",
        label: bool | None = None,
        start_angle: int = 0,
        end_angle: int = 360,
        padding_angle: int = 0,
        corner_radius: int | str | None = None,
        min_angle: int = 0,
        label_line: bool | dict[str, Any] | None = None,
        legend_type: str | None = None,
        active_shape: dict[str, Any] | None = None,
        inactive_shape: dict[str, Any] | None = None,
        is_animation_active: bool | Literal["auto"] = "auto",
        animation_begin: int = 0,
        animation_duration: int = 1500,
        animation_easing: str = "ease",
        hide: bool = False,
        **kwargs: Any,
    ):
        kw_children = kwargs.pop("children", None)
        super().__init__(**kwargs)
        self.data = data
        self.data_key = data_key
        self.name_key = name_key
        self.cx = cx
        self.cy = cy
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.label = label
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.padding_angle = padding_angle
        self.corner_radius = corner_radius
        self.min_angle = min_angle
        self.label_line = label_line
        self.legend_type = legend_type
        self.active_shape = active_shape
        self.inactive_shape = inactive_shape
        self.is_animation_active = is_animation_active
        self.animation_begin = animation_begin
        self.animation_duration = animation_duration
        self.animation_easing = animation_easing
        self.hide = hide

        self.children = list(children)
        if kw_children:
            if isinstance(kw_children, list):
                self.children.extend(kw_children)
            else:
                self.children.append(kw_children)
        self.extra_props = kwargs

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "data": self.data,
                "data_key": self.data_key,
                "name_key": self.name_key,
                "cx": self.cx,
                "cy": self.cy,
                "inner_radius": self.inner_radius,
                "outer_radius": self.outer_radius,
                "label": self.label,
                "start_angle": self.start_angle,
                "end_angle": self.end_angle,
                "paddingAngle": self.padding_angle,
                "cornerRadius": self.corner_radius,
                "minAngle": self.min_angle,
                "labelLine": self.label_line,
                "legend_type": self.legend_type,
                "activeShape": self.active_shape,
                "inactiveShape": self.inactive_shape,
                "isAnimationActive": self.is_animation_active,
                "animationBegin": self.animation_begin,
                "animation_duration": self.animation_duration,
                "animationEasing": self.animation_easing,
                "hide": self.hide,
                **self.extra_props,
            },
            "children": [c.render() for c in self.children],
        }


class PieLabel(Component):
    """Label configuration component for Pie."""

    component_type: str = "PieLabel"

    def __init__(
        self,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.props = kwargs

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                **self.props,
            },
        }


class Sector(Component):
    """Sector component for custom active shape."""

    component_type: str = "Sector"

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.props = kwargs

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": self.props,
        }


