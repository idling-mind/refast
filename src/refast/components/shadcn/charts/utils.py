"""Chart utilities."""

from typing import Any, Literal

from refast.components.base import Component
from refast.events.types import Callback


class XAxis(Component):
    """
    X-axis component.

    Args:
        data_key: Data key for axis values
        orientation: Axis orientation
        type: Axis type
        hide: Hide the axis
        tick_line: Show tick lines
        axis_line: Show axis line
        tick_margin: Margin for ticks
        x_axis_id: Unique axis ID
        height: Axis height
        width: Axis width
        allow_decimals: Allow decimal ticks
        allow_data_overflow: Allow overflow
        allow_duplicated_category: Allow duplicate categories
        scale: Scale type
        domain: Axis domain
        ticks: Custom tick values
        tick_count: Number of ticks
        tick_size: Tick size
        tick: Tick configuration
        interval: Tick interval
        padding: Left/right padding
        mirror: Mirror axis
        reversed: Reverse axis
        label: Axis label
        angle: Tick rotation angle
        min_tick_gap: Minimum gap between ticks
        unit: Unit for axis
        name: Name for axis
    """

    component_type: str = "XAxis"

    def __init__(
        self,
        data_key: str | None = None,
        orientation: Literal["top", "bottom"] = "bottom",
        type: Literal["number", "category"] = "category",
        hide: bool = False,
        tick_line: bool = True,
        axis_line: bool = True,
        tick_margin: int = 0,
        x_axis_id: str | int | None = None,
        height: int | None = None,
        width: int | None = None,
        allow_decimals: bool = True,
        allow_data_overflow: bool = False,
        allow_duplicated_category: bool = True,
        scale: str = "auto",
        domain: list[Any] | None = None,
        ticks: list[Any] | None = None,
        tick_count: int | None = None,
        tick_size: int = 6,
        tick: bool | dict[str, Any] = True,
        interval: int | str = "preserveEnd",
        padding: dict[str, int] | None = None,
        mirror: bool = False,
        reversed: bool = False,
        label: str | dict[str, Any] | None = None,
        angle: int | None = None,
        min_tick_gap: int = 5,
        unit: str | None = None,
        name: str | None = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.data_key = data_key
        self.orientation = orientation
        self.type = type
        self.hide = hide
        self.tick_line = tick_line
        self.axis_line = axis_line
        self.tick_margin = tick_margin
        self.x_axis_id = x_axis_id
        self.height = height
        self.width = width
        self.allow_decimals = allow_decimals
        self.allow_data_overflow = allow_data_overflow
        self.allow_duplicated_category = allow_duplicated_category
        self.scale = scale
        self.domain = domain
        self.ticks = ticks
        self.tick_count = tick_count
        self.tick_size = tick_size
        self.tick = tick
        self.interval = interval
        self.padding = padding
        self.mirror = mirror
        self.reversed = reversed
        self.label = label
        self.angle = angle
        self.min_tick_gap = min_tick_gap
        self.unit = unit
        self.name = name
        self.extra_props = kwargs

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "dataKey": self.data_key,
                "orientation": self.orientation,
                "type": self.type,
                "hide": self.hide,
                "tickLine": self.tick_line,
                "axisLine": self.axis_line,
                "tickMargin": self.tick_margin,
                "xAxisId": self.x_axis_id,
                "height": self.height,
                "width": self.width,
                "allowDecimals": self.allow_decimals,
                "allowDataOverflow": self.allow_data_overflow,
                "allowDuplicatedCategory": self.allow_duplicated_category,
                "scale": self.scale,
                "domain": self.domain,
                "ticks": self.ticks,
                "tickCount": self.tick_count,
                "tickSize": self.tick_size,
                "tick": self.tick,
                "interval": self.interval,
                "padding": self.padding,
                "mirror": self.mirror,
                "reversed": self.reversed,
                "label": self.label,
                "angle": self.angle,
                "minTickGap": self.min_tick_gap,
                "unit": self.unit,
                "name": self.name,
                **self.extra_props,
            },
        }


class YAxis(Component):
    """
    Y-axis component.

    Args:
        data_key: Data key for axis values
        orientation: Axis orientation
        type: Axis type
        hide: Hide the axis
        tick_line: Show tick lines
        axis_line: Show axis line
        tick_margin: Margin for ticks
        y_axis_id: Unique axis ID
        width: Axis width
        height: Axis height
        allow_decimals: Allow decimal ticks
        allow_data_overflow: Allow overflow
        allow_duplicated_category: Allow duplicate categories
        scale: Scale type
        domain: Axis domain
        ticks: Custom tick values
        tick_count: Number of ticks
        tick_size: Tick size
        tick: Tick configuration
        interval: Tick interval
        padding: Top/bottom padding
        mirror: Mirror axis
        reversed: Reverse axis
        label: Axis label
        angle: Tick rotation angle
        min_tick_gap: Minimum gap between ticks
        unit: Unit for axis
        name: Name for axis
    """

    component_type: str = "YAxis"

    def __init__(
        self,
        data_key: str | None = None,
        orientation: Literal["left", "right"] = "left",
        type: Literal["number", "category"] = "number",
        hide: bool = False,
        tick_line: bool = True,
        axis_line: bool = True,
        tick_margin: int = 0,
        y_axis_id: str | int | None = None,
        width: int | str = 60,
        height: int | None = None,
        allow_decimals: bool = True,
        allow_data_overflow: bool = False,
        allow_duplicated_category: bool = True,
        scale: str = "auto",
        domain: list[Any] | None = None,
        ticks: list[Any] | None = None,
        tick_count: int | None = None,
        tick_size: int = 6,
        tick: bool | dict[str, Any] = True,
        interval: int | str = "preserveEnd",
        padding: dict[str, int] | None = None,
        mirror: bool = False,
        reversed: bool = False,
        label: str | dict[str, Any] | None = None,
        angle: int | None = None,
        min_tick_gap: int = 5,
        unit: str | None = None,
        name: str | None = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.data_key = data_key
        self.orientation = orientation
        self.type = type
        self.hide = hide
        self.tick_line = tick_line
        self.axis_line = axis_line
        self.tick_margin = tick_margin
        self.y_axis_id = y_axis_id
        self.width = width
        self.height = height
        self.allow_decimals = allow_decimals
        self.allow_data_overflow = allow_data_overflow
        self.allow_duplicated_category = allow_duplicated_category
        self.scale = scale
        self.domain = domain
        self.ticks = ticks
        self.tick_count = tick_count
        self.tick_size = tick_size
        self.tick = tick
        self.interval = interval
        self.padding = padding
        self.mirror = mirror
        self.reversed = reversed
        self.label = label
        self.angle = angle
        self.min_tick_gap = min_tick_gap
        self.unit = unit
        self.name = name
        self.extra_props = kwargs

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "dataKey": self.data_key,
                "orientation": self.orientation,
                "type": self.type,
                "hide": self.hide,
                "tickLine": self.tick_line,
                "axisLine": self.axis_line,
                "tickMargin": self.tick_margin,
                "yAxisId": self.y_axis_id,
                "width": self.width,
                "height": self.height,
                "allowDecimals": self.allow_decimals,
                "allowDataOverflow": self.allow_data_overflow,
                "allowDuplicatedCategory": self.allow_duplicated_category,
                "scale": self.scale,
                "domain": self.domain,
                "ticks": self.ticks,
                "tickCount": self.tick_count,
                "tickSize": self.tick_size,
                "tick": self.tick,
                "interval": self.interval,
                "padding": self.padding,
                "mirror": self.mirror,
                "reversed": self.reversed,
                "label": self.label,
                "angle": self.angle,
                "minTickGap": self.min_tick_gap,
                "unit": self.unit,
                "name": self.name,
                **self.extra_props,
            },
        }


class CartesianGrid(Component):
    """
    Cartesian grid component.

    Args:
        stroke_dasharray: Dash pattern for grid lines
        vertical: Show vertical grid lines
        horizontal: Show horizontal grid lines
        x: X position
        y: Y position
        width: Grid width
        height: Grid height
        horizontal_points: Custom horizontal line positions
        vertical_points: Custom vertical line positions
        horizontal_fill: Stripe fill colors for horizontal bands
        vertical_fill: Stripe fill colors for vertical bands
        fill: Background fill
        fill_opacity: Fill opacity
        stroke: Line color
        sync_with_ticks: Sync with axis ticks
        x_axis_id: XAxis reference
        y_axis_id: YAxis reference
    """

    component_type: str = "CartesianGrid"

    def __init__(
        self,
        stroke_dasharray: str | None = None,
        vertical: bool = True,
        horizontal: bool = True,
        x: int | None = None,
        y: int | None = None,
        width: int | None = None,
        height: int | None = None,
        horizontal_points: list[int] | None = None,
        vertical_points: list[int] | None = None,
        horizontal_fill: list[str] | None = None,
        vertical_fill: list[str] | None = None,
        fill: str | None = None,
        fill_opacity: float | None = None,
        stroke: str | None = None,
        sync_with_ticks: bool = False,
        x_axis_id: str | int | None = None,
        y_axis_id: str | int | None = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.stroke_dasharray = stroke_dasharray
        self.vertical = vertical
        self.horizontal = horizontal
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.horizontal_points = horizontal_points
        self.vertical_points = vertical_points
        self.horizontal_fill = horizontal_fill
        self.vertical_fill = vertical_fill
        self.fill = fill
        self.fill_opacity = fill_opacity
        self.stroke = stroke
        self.sync_with_ticks = sync_with_ticks
        self.x_axis_id = x_axis_id
        self.y_axis_id = y_axis_id
        self.extra_props = kwargs

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "strokeDasharray": self.stroke_dasharray,
                "vertical": self.vertical,
                "horizontal": self.horizontal,
                "x": self.x,
                "y": self.y,
                "width": self.width,
                "height": self.height,
                "horizontalPoints": self.horizontal_points,
                "verticalPoints": self.vertical_points,
                "horizontalFill": self.horizontal_fill,
                "verticalFill": self.vertical_fill,
                "fill": self.fill,
                "fillOpacity": self.fill_opacity,
                "stroke": self.stroke,
                "syncWithTicks": self.sync_with_ticks,
                "xAxisId": self.x_axis_id,
                "yAxisId": self.y_axis_id,
                **self.extra_props,
            },
        }


class ReferenceLine(Component):
    """
    Reference line component.

    Args:
        y: Y coordinate for horizontal line
        x: X coordinate for vertical line
        stroke: Line color
        stroke_dasharray: Dash pattern
        stroke_width: Line width
        label: Label text or configuration
        x_axis_id: XAxis reference
        y_axis_id: YAxis reference
        if_overflow: Behavior when overflow ("discard", "hidden", "visible", "extendDomain")
        segment: Line segment points
        position: Position in band ("start", "middle", "end")
    """

    component_type: str = "ReferenceLine"

    def __init__(
        self,
        y: int | float | None = None,
        x: int | float | str | None = None,
        stroke: str | None = None,
        stroke_dasharray: str | None = None,
        stroke_width: int | None = None,
        label: str | dict[str, Any] | None = None,
        x_axis_id: str | int | None = None,
        y_axis_id: str | int | None = None,
        if_overflow: Literal["discard", "hidden", "visible", "extendDomain"] = "discard",
        segment: list[dict[str, Any]] | None = None,
        position: Literal["start", "middle", "end"] | None = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.y = y
        self.x = x
        self.stroke = stroke
        self.stroke_dasharray = stroke_dasharray
        self.stroke_width = stroke_width
        self.label = label
        self.x_axis_id = x_axis_id
        self.y_axis_id = y_axis_id
        self.if_overflow = if_overflow
        self.segment = segment
        self.position = position
        self.extra_props = kwargs

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "y": self.y,
                "x": self.x,
                "stroke": self.stroke,
                "strokeDasharray": self.stroke_dasharray,
                "strokeWidth": self.stroke_width,
                "label": self.label,
                "xAxisId": self.x_axis_id,
                "yAxisId": self.y_axis_id,
                "ifOverflow": self.if_overflow,
                "segment": self.segment,
                "position": self.position,
                **self.extra_props,
            },
        }


class ReferenceArea(Component):
    """
    Reference area component for highlighting regions.

    Args:
        x1: Start X coordinate
        x2: End X coordinate
        y1: Start Y coordinate
        y2: End Y coordinate
        x_axis_id: XAxis reference
        y_axis_id: YAxis reference
        if_overflow: Behavior when overflow
        fill: Fill color
        fill_opacity: Fill opacity
        stroke: Stroke color
        stroke_width: Stroke width
        stroke_dasharray: Dash pattern
        label: Label configuration
    """

    component_type: str = "ReferenceArea"

    def __init__(
        self,
        x1: int | str | None = None,
        x2: int | str | None = None,
        y1: int | str | None = None,
        y2: int | str | None = None,
        x_axis_id: str | int | None = None,
        y_axis_id: str | int | None = None,
        if_overflow: Literal["discard", "hidden", "visible", "extendDomain"] = "discard",
        fill: str = "#ccc",
        fill_opacity: float = 0.5,
        stroke: str | None = None,
        stroke_width: int | None = None,
        stroke_dasharray: str | None = None,
        label: str | dict[str, Any] | None = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.x_axis_id = x_axis_id
        self.y_axis_id = y_axis_id
        self.if_overflow = if_overflow
        self.fill = fill
        self.fill_opacity = fill_opacity
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.stroke_dasharray = stroke_dasharray
        self.label = label
        self.extra_props = kwargs

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "x1": self.x1,
                "x2": self.x2,
                "y1": self.y1,
                "y2": self.y2,
                "xAxisId": self.x_axis_id,
                "yAxisId": self.y_axis_id,
                "ifOverflow": self.if_overflow,
                "fill": self.fill,
                "fillOpacity": self.fill_opacity,
                "stroke": self.stroke,
                "strokeWidth": self.stroke_width,
                "strokeDasharray": self.stroke_dasharray,
                "label": self.label,
                **self.extra_props,
            },
        }


class ReferenceDot(Component):
    """
    Reference dot component.

    Args:
        x: X coordinate
        y: Y coordinate
        r: Radius
        x_axis_id: XAxis reference
        y_axis_id: YAxis reference
        if_overflow: Behavior when overflow
        fill: Fill color
        stroke: Stroke color
        stroke_width: Stroke width
        label: Label configuration
    """

    component_type: str = "ReferenceDot"

    def __init__(
        self,
        x: int | str | None = None,
        y: int | str | None = None,
        r: int = 10,
        x_axis_id: str | int | None = None,
        y_axis_id: str | int | None = None,
        if_overflow: Literal["discard", "hidden", "visible", "extendDomain"] = "discard",
        fill: str = "#fff",
        stroke: str = "#ccc",
        stroke_width: int = 1,
        label: str | dict[str, Any] | None = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.x = x
        self.y = y
        self.r = r
        self.x_axis_id = x_axis_id
        self.y_axis_id = y_axis_id
        self.if_overflow = if_overflow
        self.fill = fill
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.label = label
        self.extra_props = kwargs

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "x": self.x,
                "y": self.y,
                "r": self.r,
                "xAxisId": self.x_axis_id,
                "yAxisId": self.y_axis_id,
                "ifOverflow": self.if_overflow,
                "fill": self.fill,
                "stroke": self.stroke,
                "strokeWidth": self.stroke_width,
                "label": self.label,
                **self.extra_props,
            },
        }


class Brush(Component):
    """
    Brush component for zooming and panning.

    Args:
        data_key: Data key for brush display
        height: Brush height
        stroke: Stroke color
        x: X position
        y: Y position
        width: Brush width
        traveller_width: Handle width
        gap: Data skip gap
        start_index: Initial start index
        end_index: Initial end index
        fill: Fill color
        padding: Padding
        always_show_text: Always show text labels
        on_change: Change event handler
    """

    component_type: str = "Brush"

    def __init__(
        self,
        data_key: str | None = None,
        height: int = 30,
        stroke: str | None = None,
        x: int | None = None,
        y: int | None = None,
        width: int | None = None,
        traveller_width: int = 5,
        gap: int = 1,
        start_index: int | None = None,
        end_index: int | None = None,
        fill: str | None = None,
        padding: dict[str, int] | None = None,
        always_show_text: bool = False,
        on_change: Callback | None = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.data_key = data_key
        self.height = height
        self.stroke = stroke
        self.x = x
        self.y = y
        self.width = width
        self.traveller_width = traveller_width
        self.gap = gap
        self.start_index = start_index
        self.end_index = end_index
        self.fill = fill
        self.padding = padding
        self.always_show_text = always_show_text
        self.on_change = on_change
        self.extra_props = kwargs

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "dataKey": self.data_key,
                "height": self.height,
                "stroke": self.stroke,
                "x": self.x,
                "y": self.y,
                "width": self.width,
                "travellerWidth": self.traveller_width,
                "gap": self.gap,
                "startIndex": self.start_index,
                "endIndex": self.end_index,
                "fill": self.fill,
                "padding": self.padding,
                "alwaysShowText": self.always_show_text,
                "onChange": self.on_change.serialize() if self.on_change else None,
                **self.extra_props,
            },
        }


class Cell(Component):
    """
    Cell component for individual styling in Pie/Bar charts.

    Args:
        fill: Fill color
        stroke: Stroke color
    """

    component_type: str = "Cell"

    def __init__(
        self,
        fill: str | None = None,
        stroke: str | None = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.fill = fill
        self.stroke = stroke
        self.extra_props = kwargs

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "fill": self.fill,
                "stroke": self.stroke,
                **self.extra_props,
            },
        }


class LabelList(Component):
    """
    LabelList component for data labels on chart elements.

    Args:
        data_key: Data key for label values
        position: Label position
        offset: Position offset
        angle: Rotation angle
        fill: Text color
        font_size: Font size
    """

    component_type: str = "LabelList"

    def __init__(
        self,
        data_key: str | None = None,
        position: str = "top",
        offset: int = 5,
        angle: int = 0,
        fill: str = "#333",
        font_size: int | str = 12,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.data_key = data_key
        self.position = position
        self.offset = offset
        self.angle = angle
        self.fill = fill
        self.font_size = font_size
        self.extra_props = kwargs

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "dataKey": self.data_key,
                "position": self.position,
                "offset": self.offset,
                "angle": self.angle,
                "fill": self.fill,
                "fontSize": self.font_size,
                **self.extra_props,
            },
        }


class Label(Component):
    """
    Label component for chart annotations.

    Args:
        value: Label text value
        position: Label position
        offset: Position offset
        angle: Rotation angle
        fill: Text color
        font_size: Font size
    """

    component_type: str = "ChartLabel"

    def __init__(
        self,
        value: str | int | None = None,
        position: str = "center",
        offset: int = 0,
        angle: int = 0,
        fill: str = "#333",
        font_size: int | str = 12,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.value = value
        self.position = position
        self.offset = offset
        self.angle = angle
        self.fill = fill
        self.font_size = font_size
        self.extra_props = kwargs

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "value": self.value,
                "position": self.position,
                "offset": self.offset,
                "angle": self.angle,
                "fill": self.fill,
                "fontSize": self.font_size,
                **self.extra_props,
            },
        }


class ErrorBar(Component):
    """
    ErrorBar component for displaying data uncertainty.

    Args:
        data_key: Data key for error values
        width: Bar end width
        direction: Direction ("x" or "y")
        stroke: Line color
        stroke_width: Line width
        is_animation_active: Enable animation
        animation_begin: Animation delay (ms)
        animation_duration: Animation duration (ms)
        animation_easing: Easing function
    """

    component_type: str = "ErrorBar"

    def __init__(
        self,
        data_key: str,
        width: int = 4,
        direction: Literal["x", "y"] = "y",
        stroke: str = "#333",
        stroke_width: int = 1,
        is_animation_active: bool = False,
        animation_begin: int = 0,
        animation_duration: int = 1500,
        animation_easing: str = "ease",
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.data_key = data_key
        self.width = width
        self.direction = direction
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.is_animation_active = is_animation_active
        self.animation_begin = animation_begin
        self.animation_duration = animation_duration
        self.animation_easing = animation_easing
        self.extra_props = kwargs

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "dataKey": self.data_key,
                "width": self.width,
                "direction": self.direction,
                "stroke": self.stroke,
                "strokeWidth": self.stroke_width,
                "isAnimationActive": self.is_animation_active,
                "animationBegin": self.animation_begin,
                "animationDuration": self.animation_duration,
                "animationEasing": self.animation_easing,
                **self.extra_props,
            },
        }
