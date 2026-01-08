"""Radial chart components."""

from typing import Any
from refast.components.base import Component


class RadialBarChart(Component):
    """
    Radial bar chart component.
    
    Example:
        ```python
        RadialBarChart(
            data=data,
            inner_radius="10%",
            outer_radius="80%",
            RadialBar(background=True, data_key="uv"),
        )
        ```
    """
    
    component_type: str = "RadialBarChart"
    
    def __init__(
        self,
        *children: Component,
        data: list[dict[str, Any]],
        margin: dict[str, int] | None = None,
        cx: str | int = "50%",
        cy: str | int = "50%",
        inner_radius: int | str = "10%",
        outer_radius: int | str = "80%",
        bar_size: int | None = None,
        start_angle: int = 90,
        end_angle: int = -270,
        **kwargs: Any,
    ):
        kw_children = kwargs.pop("children", None)
        super().__init__(**kwargs)
        self.data = data
        self.margin = margin or {"top": 0, "right": 0, "left": 0, "bottom": 0}
        self.cx = cx
        self.cy = cy
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.bar_size = bar_size
        self.start_angle = start_angle
        self.end_angle = end_angle
        
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
                "cx": self.cx,
                "cy": self.cy,
                "innerRadius": self.inner_radius,
                "outerRadius": self.outer_radius,
                "barSize": self.bar_size,
                "startAngle": self.start_angle,
                "endAngle": self.end_angle,
            },
            "children": [c.render() for c in self.children],
        }


class RadialBar(Component):
    """
    Radial bar component for RadialBarChart.
    
    Args:
        data_key: Key from data
        min_angle: Minimum angle
        background: Whether to show background track
        label: Label configuration
        corner_radius: Corner radius
    """
    
    component_type: str = "RadialBar"
    
    def __init__(
        self,
        data_key: str,
        min_angle: int = 0,
        background: bool | dict[str, Any] = False,
        label: bool | dict[str, Any] | None = None,
        corner_radius: int | str | None = None,
        fill: str = "hsl(var(--chart-1))",
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.data_key = data_key
        self.min_angle = min_angle
        self.background = background
        self.label = label
        self.corner_radius = corner_radius
        self.fill = fill
        self.props = kwargs
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "dataKey": self.data_key,
                "minAngle": self.min_angle,
                "background": self.background,
                "label": self.label,
                "cornerRadius": self.corner_radius,
                "fill": self.fill,
                **self.props,
            },
        }
