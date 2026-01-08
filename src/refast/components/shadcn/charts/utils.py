"""Chart utilities."""

from typing import Any, Literal
from refast.components.base import Component


class XAxis(Component):
    """X-axis component."""
    
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
        self.props = kwargs
    
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
                **self.props,
            },
        }

class YAxis(Component):
    """Y-axis component."""
    
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
        self.props = kwargs
    
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
                **self.props,
            },
        }

class CartesianGrid(Component):
    """Cartesian grid component."""
    
    component_type: str = "CartesianGrid"
    
    def __init__(
        self,
        stroke_dasharray: str | None = None,
        vertical: bool = True,
        horizontal: bool = True,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.stroke_dasharray = stroke_dasharray
        self.vertical = vertical
        self.horizontal = horizontal
        self.props = kwargs
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "strokeDasharray": self.stroke_dasharray,
                "vertical": self.vertical,
                "horizontal": self.horizontal,
                **self.props,
            },
        }

class ReferenceLine(Component):
    """Reference line component."""
    
    component_type: str = "ReferenceLine"
    
    def __init__(
        self,
        y: int | float | None = None,
        x: int | float | str | None = None,
        stroke: str | None = None,
        stroke_dasharray: str | None = None,
        label: str | None = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.y = y
        self.x = x
        self.stroke = stroke
        self.stroke_dasharray = stroke_dasharray
        self.label = label
        self.props = kwargs
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "y": self.y,
                "x": self.x,
                "stroke": self.stroke,
                "strokeDasharray": self.stroke_dasharray,
                "label": self.label,
                **self.props,
            },
        }

class Brush(Component):
    """Brush component for zooming."""
    
    component_type: str = "Brush"
    
    def __init__(
        self,
        data_key: str | None = None,
        height: int = 30,
        stroke: str | None = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.data_key = data_key
        self.height = height
        self.stroke = stroke
        self.props = kwargs
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "dataKey": self.data_key,
                "height": self.height,
                "stroke": self.stroke,
                **self.props,
            },
        }
