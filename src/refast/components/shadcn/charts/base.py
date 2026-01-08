"""Base chart components and utilities."""

from typing import Any, Literal
from pydantic import BaseModel, Field
from refast.components.base import Component


class ChartConfig(BaseModel):
    """Configuration for chart data series."""
    
    label: str
    color: str | None = None
    icon: str | None = None
    
    class Config:
        extra = "allow"


class ChartStyle(Component):
    """
    Style component for chart theming.
    
    Generates CSS custom properties for chart colors.
    """
    
    component_type: str = "ChartStyle"
    
    def __init__(
        self,
        id: str,
        config: dict[str, ChartConfig],
        **kwargs: Any,
    ):
        super().__init__(id=id, **kwargs)
        self.config = config
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "id": self.id,
                "config": {k: v.model_dump() for k, v in self.config.items()},
            },
        }


class ChartContainer(Component):
    """
    Container component for charts.
    
    Provides responsive sizing and theming context.
    
    Example:
        ```python
        ChartContainer(
            config={
                "desktop": ChartConfig(label="Desktop", color="hsl(var(--chart-1))"),
                "mobile": ChartConfig(label="Mobile", color="hsl(var(--chart-2))"),
            },
            AreaChart(
                data=data,
                Area(data_key="desktop", fill="var(--color-desktop)"),
                Area(data_key="mobile", fill="var(--color-mobile)"),
            ),
        )
        ```
    """
    
    component_type: str = "ChartContainer"
    
    def __init__(
        self,
        *children: Component,
        config: dict[str, ChartConfig] | None = None,
        class_name: str = "",
        aspect_ratio: float | None = None,
        min_height: int | str = 200,
        **kwargs: Any,
    ):
        # Extract children from kwargs if present
        kw_children = kwargs.pop("children", None)

        super().__init__(class_name=class_name, **kwargs)
        self.config = config or {}
        self.aspect_ratio = aspect_ratio
        self.min_height = min_height
        
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
                "config": {k: v.model_dump() for k, v in self.config.items()},
                "className": self.class_name,
                "aspectRatio": self.aspect_ratio,
                "minHeight": self.min_height,
            },
            "children": [c.render() for c in self.children],
        }


class ChartTooltip(Component):
    """
    Tooltip component for charts.
    
    Example:
        ```python
        ChartTooltip(
            cursor=True,
            content=ChartTooltipContent(indicator="line"),
        )
        ```
    """
    
    component_type: str = "ChartTooltip"
    
    def __init__(
        self,
        content: "ChartTooltipContent | None" = None,
        cursor: bool = True,
        hide_label: bool = False,
        hide_indicator: bool = False,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.content = content
        self.cursor = cursor
        self.hide_label = hide_label
        self.hide_indicator = hide_indicator
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "cursor": self.cursor,
                "hideLabel": self.hide_label,
                "hideIndicator": self.hide_indicator,
            },
            "children": [self.content.render()] if self.content else [],
        }


class ChartTooltipContent(Component):
    """
    Content component for chart tooltips.
    
    Args:
        indicator: Type of indicator ("line" | "dot" | "dashed")
        name_key: Key to use for the name
        label_key: Key to use for the label
    """
    
    component_type: str = "ChartTooltipContent"
    
    def __init__(
        self,
        indicator: Literal["line", "dot", "dashed"] = "dot",
        name_key: str | None = None,
        label_key: str | None = None,
        hide_label: bool = False,
        hide_indicator: bool = False,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.indicator = indicator
        self.name_key = name_key
        self.label_key = label_key
        self.hide_label = hide_label
        self.hide_indicator = hide_indicator
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "indicator": self.indicator,
                "nameKey": self.name_key,
                "labelKey": self.label_key,
                "hideLabel": self.hide_label,
                "hideIndicator": self.hide_indicator,
            },
        }


class ChartLegend(Component):
    """
    Legend component for charts.
    
    Example:
        ```python
        ChartLegend(content=ChartLegendContent())
        ```
    """
    
    component_type: str = "ChartLegend"
    
    def __init__(
        self,
        content: "ChartLegendContent | None" = None,
        vertical_align: Literal["top", "middle", "bottom"] = "bottom",
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.content = content
        self.vertical_align = vertical_align
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "verticalAlign": self.vertical_align,
            },
            "children": [self.content.render()] if self.content else [],
        }


class ChartLegendContent(Component):
    """Content component for chart legends."""
    
    component_type: str = "ChartLegendContent"
    
    def __init__(
        self,
        name_key: str | None = None,
        hide_icon: bool = False,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.name_key = name_key
        self.hide_icon = hide_icon
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "nameKey": self.name_key,
                "hideIcon": self.hide_icon,
            },
        }
