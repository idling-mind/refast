"""Bar chart components."""

from typing import Any, Literal

from refast.components.base import Component
from refast.context import Callback


class BarChart(Component):
    """
    Bar chart component.

    Example:
        ```python
        BarChart(
            data=data,
            Bar(data_key="items", fill="hsl(var(--chart-1))"),
        )
        ```

    Args:
        data: List of data dictionaries
        margin: Chart margins
        bar_category_gap: Gap between bar categories
        bar_gap: Gap between bars in same category
        bar_size: Default bar size
        layout: Chart layout direction
        stack_offset: Stack offset type
        sync_id: ID for syncing multiple charts
        sync_method: How to sync charts
        reverse_stack_order: Reverse stacking order
        max_bar_size: Maximum bar width
        on_click: Click event handler
        on_mouse_enter: Mouse enter handler
        on_mouse_leave: Mouse leave handler
        on_mouse_move: Mouse move handler
    """

    component_type: str = "BarChart"

    def __init__(
        self,
        *children: Component | str | None,
        data: list[dict[str, Any]],
        margin: dict[str, int] | None = None,
        bar_category_gap: str | int | None = None,
        bar_gap: str | int | None = None,
        bar_size: int | None = None,
        layout: Literal["horizontal", "vertical"] = "horizontal",
        stack_offset: Literal["expand", "none", "wiggle", "silhouette", "sign"] = "none",
        sync_id: str | None = None,
        sync_method: Literal["index", "value"] | None = None,
        reverse_stack_order: bool = False,
        max_bar_size: int | None = None,
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
        self.bar_category_gap = bar_category_gap
        self.bar_gap = bar_gap
        self.bar_size = bar_size
        self.layout = layout
        self.stack_offset = stack_offset
        self.sync_id = sync_id
        self.sync_method = sync_method
        self.reverse_stack_order = reverse_stack_order
        self.max_bar_size = max_bar_size
        self.on_click = on_click
        self.on_mouse_enter = on_mouse_enter
        self.on_mouse_leave = on_mouse_leave
        self.on_mouse_move = on_mouse_move

        self.add_children(list(children))
        self.add_children(kw_children)

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "data": self.data,
                "margin": self.margin,
                "bar_category_gap": self.bar_category_gap,
                "bar_size": self.bar_size,
                "bar_gap": self.bar_gap,
                "layout": self.layout,
                "stackOffset": self.stack_offset,
                "syncId": self.sync_id,
                "syncMethod": self.sync_method,
                "reverseStackOrder": self.reverse_stack_order,
                "maxBarSize": self.max_bar_size,
                "on_click": self.on_click.serialize() if self.on_click else None,
                "on_mouse_enter": (
                    self.on_mouse_enter.serialize() if self.on_mouse_enter else None
                ),
                "on_mouse_leave": (
                    self.on_mouse_leave.serialize() if self.on_mouse_leave else None
                ),
                "on_mouse_move": (self.on_mouse_move.serialize() if self.on_mouse_move else None),
            },
            "children": self._render_children(),
        }


class Bar(Component):
    """
    Bar component for BarChart.

    Args:
        data_key: Key from data
        fill: Fill color
        radius: Border radius of bar
        bar_size: Bar size
        bar_gap: Gap between bars
        stack_id: Stack ID for stacked bars
        background: Whether to show background
        x_axis_id: XAxis reference
        y_axis_id: YAxis reference
        min_point_size: Minimum bar height for 0 values
        max_bar_size: Maximum bar size
        name: Name for tooltip/legend
        unit: Unit for tooltip
        legend_type: Legend icon type
        label: Label configuration
        active_bar: Active bar styling
        is_animation_active: Enable animation
        animation_begin: Animation delay (ms)
        animation_duration: Animation duration (ms)
        animation_easing: Easing function
        hide: Hide the bar
    """

    component_type: str = "Bar"

    def __init__(
        self,
        data_key: str,
        fill: str = "hsl(var(--chart-1))",
        radius: int | list[int] = 0,
        bar_size: int | None = None,
        bar_gap: str | int | None = None,
        stack_id: str | None = None,
        background: bool | dict[str, Any] = False,
        x_axis_id: str | int | None = None,
        y_axis_id: str | int | None = None,
        min_point_size: int | None = None,
        max_bar_size: int | None = None,
        name: str | None = None,
        unit: str | None = None,
        legend_type: str | None = None,
        label: bool | dict[str, Any] | None = None,
        active_bar: bool | dict[str, Any] | None = None,
        is_animation_active: bool | Literal["auto"] = "auto",
        animation_begin: int = 0,
        animation_duration: int = 1500,
        animation_easing: str = "ease",
        hide: bool = False,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.data_key = data_key
        self.fill = fill
        self.radius = radius
        self.bar_size = bar_size
        self.bar_gap = bar_gap
        self.stack_id = stack_id
        self.background = background
        self.x_axis_id = x_axis_id
        self.y_axis_id = y_axis_id
        self.min_point_size = min_point_size
        self.max_bar_size = max_bar_size
        self.name = name
        self.unit = unit
        self.legend_type = legend_type
        self.label = label
        self.active_bar = active_bar
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
                "fill": self.fill,
                "radius": self.radius,
                "bar_size": self.bar_size,
                "stack_id": self.stack_id,
                "background": self.background,
                "x_axis_id": self.x_axis_id,
                "y_axis_id": self.y_axis_id,
                "minPointSize": self.min_point_size,
                "maxBarSize": self.max_bar_size,
                "name": self.name,
                "unit": self.unit,
                "legend_type": self.legend_type,
                "label": self.label,
                "activeBar": self.active_bar,
                "isAnimationActive": self.is_animation_active,
                "animationBegin": self.animation_begin,
                "animation_duration": self.animation_duration,
                "animationEasing": self.animation_easing,
                "hide": self.hide,
                **self.extra_props,
            },
        }
