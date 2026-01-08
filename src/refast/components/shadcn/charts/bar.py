"""Bar chart components."""

from typing import Any, Literal
from refast.components.base import Component


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
    """
    
    component_type: str = "BarChart"
    
    def __init__(
        self,
        *children: Component,
        data: list[dict[str, Any]],
        margin: dict[str, int] | None = None,
        bar_category_gap: str | int | None = None,
        bar_gap: str | int | None = None,
        bar_size: int | None = None,
        layout: Literal["horizontal", "vertical"] = "horizontal",
        stack_offset: Literal["expand", "none", "wiggle", "silhouette", "sign"] = "none",
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
                "barCategoryGap": self.bar_category_gap,
                "barGap": self.bar_gap,
                "barSize": self.bar_size,
                "layout": self.layout,
                "stackOffset": self.stack_offset,
            },
            "children": [c.render() for c in self.children],
        }


class Bar(Component):
    """
    Bar component for BarChart.
    
    Args:
        data_key: Key from data
        fill: Fill color
        radius: Border radius of bar
        stack_id: Stack ID for stacked bars
    """
    
    component_type: str = "Bar"
    
    def __init__(
        self,
        data_key: str,
        fill: str = "hsl(var(--chart-1))",
        radius: int | list[int] = 0,
        bar_size: int | None = None,
        stack_id: str | None = None,
        background: bool | dict[str, Any] = False,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.data_key = data_key
        self.fill = fill
        self.radius = radius
        self.bar_size = bar_size
        self.stack_id = stack_id
        self.background = background
        self.props = kwargs
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "dataKey": self.data_key,
                "fill": self.fill,
                "radius": self.radius,
                "barSize": self.bar_size,
                "stackId": self.stack_id,
                "background": self.background,
                **self.props,
            },
        }
