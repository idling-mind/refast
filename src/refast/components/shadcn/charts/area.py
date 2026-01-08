"""Area chart components."""

from typing import Any, Literal
from refast.components.base import Component


class AreaChart(Component):
    """
    Area chart component.
    
    Example:
        ```python
        AreaChart(
            data=data,
            margin={"top": 10, "right": 10, "left": 10, "bottom": 0},
            Area(data_key="value", fill="hsl(var(--chart-1))"),
        )
        ```
    """
    
    component_type: str = "AreaChart"
    
    def __init__(
        self,
        *children: Component,
        data: list[dict[str, Any]],
        margin: dict[str, int] | None = None,
        stack_offset: Literal["expand", "none", "wiggle", "silhouette"] | None = None,
        **kwargs: Any,
    ):
        kw_children = kwargs.pop("children", None)
        super().__init__(**kwargs)
        self.data = data
        self.margin = margin or {"top": 10, "right": 10, "left": 10, "bottom": 0}
        self.stack_offset = stack_offset
        
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
    """
    
    component_type: str = "Area"
    
    def __init__(
        self,
        data_key: str,
        type: Literal["basis", "linear", "natural", "monotone", "step", "stepBefore", "stepAfter"] = "natural",
        fill: str = "hsl(var(--chart-1))",
        fill_opacity: float = 0.4,
        stroke: str | None = None,
        stroke_width: int = 2,
        stacked_id: str | None = None,
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
            },
        }
