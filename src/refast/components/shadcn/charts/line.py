"""Line chart components."""

from typing import Any, Literal
from refast.components.base import Component


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
    """
    
    component_type: str = "LineChart"
    
    def __init__(
        self,
        *children: Component,
        data: list[dict[str, Any]],
        margin: dict[str, int] | None = None,
        **kwargs: Any,
    ):
        kw_children = kwargs.pop("children", None)
        super().__init__(**kwargs)
        self.data = data
        self.margin = margin or {"top": 10, "right": 10, "left": 10, "bottom": 0}
        
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
    """
    
    component_type: str = "Line"
    
    def __init__(
        self,
        data_key: str,
        type: Literal["basis", "linear", "natural", "monotone", "step", "stepBefore", "stepAfter"] = "natural",
        stroke: str = "hsl(var(--chart-1))",
        stroke_width: int = 2,
        dot: bool | dict[str, Any] = True,
        active_dot: bool | dict[str, Any] = True,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.data_key = data_key
        self.type = type
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.dot = dot
        self.active_dot = active_dot
        self.props = kwargs
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "dataKey": self.data_key,
                "type": self.type,
                "stroke": self.stroke,
                "strokeWidth": self.stroke_width,
                "dot": self.dot,
                "activeDot": self.active_dot,
                **self.props,
            },
        }
