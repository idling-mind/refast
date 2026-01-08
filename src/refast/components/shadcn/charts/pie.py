"""Pie chart components."""

from typing import Any
from refast.components.base import Component


class PieChart(Component):
    """
    Pie chart component.
    
    Example:
        ```python
        PieChart(
            Pie(data=data, data_key="value", name_key="name"),
        )
        ```
    """
    
    component_type: str = "PieChart"
    
    def __init__(
        self,
        *children: Component,
        margin: dict[str, int] | None = None,
        **kwargs: Any,
    ):
        kw_children = kwargs.pop("children", None)
        super().__init__(**kwargs)
        self.margin = margin or {"top": 0, "right": 0, "left": 0, "bottom": 0}
        
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
        
        self.children = list(children)
        if kw_children:
            if isinstance(kw_children, list):
                self.children.extend(kw_children)
            else:
                self.children.append(kw_children)
        self.props = kwargs
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "data": self.data,
                "dataKey": self.data_key,
                "nameKey": self.name_key,
                "cx": self.cx,
                "cy": self.cy,
                "innerRadius": self.inner_radius,
                "outerRadius": self.outer_radius,
                "label": self.label,
                **self.props,
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
