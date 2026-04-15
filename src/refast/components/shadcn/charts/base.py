"""Base chart components and utilities."""

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

from refast.components.base import ChildrenType, Component
from refast.context import Callback


class ChartConfig(BaseModel):
    """Configuration for chart data series."""

    model_config = ConfigDict(extra="allow")

    label: str
    color: str | None = None
    icon: str | None = None


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
        extra_props: dict[str, Any] | None = None,
    ):
        super().__init__(id=id, extra_props=extra_props)
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
        children: ChildrenType = None,
        config: dict[str, ChartConfig] | None = None,
        id: str | None = None,
        class_name: str = "",
        width: str | int = "100%",
        height: str | int = "100%",
        min_height: str | int | None = 200,
        min_width: str | int | None = None,
        max_height: str | int | None = None,
        aspect: float | None = None,
        debounce: int | None = None,
        initial_dimension: dict[str, int] | None = None,
        on_resize: Callback | None = None,
        extra_props: dict[str, Any] | None = None,
    ):
        super().__init__(id=id, class_name=class_name, extra_props=extra_props)
        self.config = config or {}

        # Props
        self.width = width
        self.height = height
        self.min_height = min_height
        self.min_width = min_width
        self.max_height = max_height
        self.aspect = aspect
        self.debounce = debounce
        self.initial_dimension = initial_dimension
        self.on_resize = on_resize

        self.add_children(children)

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "config": {k: v.model_dump() for k, v in self.config.items()},
                "class_name": self.class_name,
                "style": self.style,
                "width": self.width,
                "height": self.height,
                "min_height": self.min_height,
                "min_width": self.min_width,
                "max_height": self.max_height,
                "aspect": self.aspect,
                "debounce": self.debounce,
                "initialDimension": self.initial_dimension,
                "onResize": self.on_resize.serialize() if self.on_resize else None,
                **self.extra_props,
            },
            "children": self._render_children(),
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
        id: str | None = None,
        extra_props: dict[str, Any] | None = None,
    ):
        super().__init__(id=id, extra_props=extra_props)
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
                "hide_label": self.hide_label,
                "hide_indicator": self.hide_indicator,
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
        id: str | None = None,
        extra_props: dict[str, Any] | None = None,
    ):
        super().__init__(id=id, extra_props=extra_props)
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
                "name_key": self.name_key,
                "label_key": self.label_key,
                "hide_label": self.hide_label,
                "hide_indicator": self.hide_indicator,
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
        id: str | None = None,
        extra_props: dict[str, Any] | None = None,
    ):
        super().__init__(id=id, extra_props=extra_props)
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
        id: str | None = None,
        extra_props: dict[str, Any] | None = None,
    ):
        super().__init__(id=id, extra_props=extra_props)
        self.name_key = name_key
        self.hide_icon = hide_icon

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "name_key": self.name_key,
                "hideIcon": self.hide_icon,
            },
        }
