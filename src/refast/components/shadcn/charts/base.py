"""Base chart components and utilities."""

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, model_validator

from refast.components.base import ChildrenType, Component
from refast.context import Callback


class ChartConfig(BaseModel):
    """Configuration for chart data series.

    Args:
        label: Human-readable label shown in tooltip and legend.
        color: Color for the series. Accepts:
            - ``None``: auto-assigned from the ``--chart-N`` palette by order.
            - ``int``: palette index, e.g. ``color=3`` → ``hsl(var(--chart-3))``.
            - ``str``: any CSS color, e.g. ``"#ff5500"`` or ``"hsl(var(--chart-1))"``.
        icon: Optional Lucide icon name.
    """

    model_config = ConfigDict(extra="allow")

    label: str
    color: str | None = None
    icon: str | None = None

    @model_validator(mode="before")
    @classmethod
    def _resolve_color(cls, values: Any) -> Any:
        """Convert integer color index to a CSS variable string."""
        if isinstance(values, dict) and isinstance(values.get("color"), int):
            values = dict(values)
            values["color"] = f"hsl(var(--chart-{values['color']}))"
        return values


class SeriesMixin:
    """Mixin for chart series components (Area, Bar, Line, Scatter, Radar).

    Enables :class:`ChartContainer` to auto-discover series and build a
    ``ChartConfig`` dict without any explicit ``config=`` argument.
    Subclasses set ``self.label`` and ``self.color`` in their ``__init__``.
    """

    _is_chart_series = True

    @property
    def series_key(self) -> str:
        """Key used for the ``--color-{key}`` CSS variable and config dict."""
        return getattr(self, "data_key", None) or str(self.id)  # type: ignore[attr-defined]


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

    Provides responsive sizing and theming context. Colors and labels can be
    specified directly on series components — no ``config=`` argument required:

    Example (zero-config):
        ```python
        ChartContainer(
            min_height=300,
            children=AreaChart(
                data=data,
                children=[
                    Area(data_key="desktop", label="Desktop"),
                    Area(data_key="mobile",  label="Mobile", color=2),
                ],
            ),
        )
        ```

    Example (explicit config, backward-compatible):
        ```python
        ChartContainer(
            config={
                "desktop": ChartConfig(label="Desktop", color=1),
                "mobile":  ChartConfig(label="Mobile",  color="#6366f1"),
            },
            children=...,
        )
        ```
    """

    component_type: str = "ChartContainer"

    def __init__(
        self,
        children: ChildrenType = None,
        config: "dict[str, ChartConfig | dict[str, Any] | str] | None" = None,
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
        style: dict[str, Any] | None = None,
        parent_style: dict[str, Any] | None = None,
        extra_props: dict[str, Any] | None = None,
    ):
        super().__init__(
            id=id,
            class_name=class_name,
            style=style,
            parent_style=parent_style,
            extra_props=extra_props,
        )
        self.config = self._normalize_config(config)

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

    @staticmethod
    def _normalize_config(
        config: dict | None,
    ) -> dict[str, ChartConfig]:
        """Normalize config values to :class:`ChartConfig` instances.

        Accepts ``ChartConfig``, plain ``dict``, or ``str`` (label only) as values.
        """
        if not config:
            return {}
        result: dict[str, ChartConfig] = {}
        for k, v in config.items():
            if isinstance(v, ChartConfig):
                result[k] = v
            elif isinstance(v, dict):
                result[k] = ChartConfig(**v)
            elif isinstance(v, str):
                result[k] = ChartConfig(label=v)
            else:
                result[k] = v  # type: ignore[assignment]
        return result

    def _collect_series_from_children(self) -> "list[SeriesMixin]":
        """Recursively walk the children tree and collect all series components."""
        series: list[SeriesMixin] = []

        def walk(components: list) -> None:
            for comp in components:
                if isinstance(comp, SeriesMixin):
                    series.append(comp)
                walk(comp._traversal_children())

        walk(self._traversal_children())
        return series

    def _build_config(self) -> dict[str, ChartConfig]:
        """Merge auto-discovered series config with explicit config.

        Explicit ``config=`` entries override auto-discovered ones.
        Colors are auto-assigned from the ``--chart-N`` palette in discovery
        order for any entry (auto or explicit) that has no color set.
        """
        # Step 1: auto-config from children series components
        auto_config: dict[str, ChartConfig] = {}
        for series in self._collect_series_from_children():
            key = series.series_key
            if key not in auto_config:
                auto_config[key] = ChartConfig(
                    label=getattr(series, "label", None) or key,
                    color=getattr(series, "color", None),
                )

        # Step 2: explicit config overrides auto-config per key
        merged: dict[str, ChartConfig] = {**auto_config, **self.config}

        # Step 3: auto-assign palette colors in iteration order for None-color entries
        resolved: dict[str, ChartConfig] = {}
        color_index = 0
        for key, cfg in merged.items():
            if cfg.color is None:
                color = f"hsl(var(--chart-{(color_index % 8) + 1}))"
                color_index += 1
                resolved[key] = ChartConfig(
                    label=cfg.label,
                    color=color,
                    icon=getattr(cfg, "icon", None),
                )
            else:
                resolved[key] = cfg

        return resolved

    def render(self) -> dict[str, Any]:
        config = self._build_config()
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "config": {k: v.model_dump() for k, v in config.items()},
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
                "content": self.content.render() if self.content else None,
            },
            "children": [],
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
