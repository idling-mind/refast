"""Radar chart components."""

from typing import Any

from refast.components.base import Component


class RadarChart(Component):
    """
    Radar chart component.

    Example:
        ```python
        RadarChart(
            data=data,
            Radar(data_key="value", fill="hsl(var(--chart-1))"),
        )
        ```
    """

    component_type: str = "RadarChart"

    def __init__(
        self,
        *children: Component,
        data: list[dict[str, Any]],
        margin: dict[str, int] | None = None,
        cx: str | int = "50%",
        cy: str | int = "50%",
        inner_radius: int | str | None = None,
        outer_radius: int | str = "80%",
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
                "startAngle": self.start_angle,
                "endAngle": self.end_angle,
            },
            "children": [c.render() for c in self.children],
        }


class Radar(Component):
    """
    Radar component for RadarChart.

    Args:
        data_key: Key from data
        fill: Fill color
        fill_opacity: Fill opacity
        stroke: Stroke color
        stroke_width: Stroke width
    """

    component_type: str = "Radar"

    def __init__(
        self,
        data_key: str,
        fill: str = "hsl(var(--chart-1))",
        fill_opacity: float = 0.6,
        stroke: str | None = None,
        stroke_width: int = 2,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.data_key = data_key
        self.fill = fill
        self.fill_opacity = fill_opacity
        self.stroke = stroke or fill
        self.stroke_width = stroke_width
        self.props = kwargs

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "dataKey": self.data_key,
                "fill": self.fill,
                "fillOpacity": self.fill_opacity,
                "stroke": self.stroke,
                "strokeWidth": self.stroke_width,
                **self.props,
            },
        }


class PolarGrid(Component):
    """Polar grid for RadarChart."""

    component_type: str = "PolarGrid"

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.props = kwargs

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": self.props,
        }


class PolarAngleAxis(Component):
    """Polar angle axis for RadarChart."""

    component_type: str = "PolarAngleAxis"

    def __init__(
        self,
        data_key: str | None = None,
        type: str = "category",
        tick: bool | dict[str, Any] = True,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.data_key = data_key
        self.type = type
        self.tick = tick
        self.props = kwargs

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "dataKey": self.data_key,
                "type": self.type,
                "tick": self.tick,
                **self.props,
            },
        }


class PolarRadiusAxis(Component):
    """Polar radius axis for RadarChart/RadialBarChart."""

    component_type: str = "PolarRadiusAxis"

    def __init__(
        self,
        angle: int = 90,
        type: str = "number",
        tick: bool | dict[str, Any] = True,
        domain: list[int | str] | None = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.angle = angle
        self.type = type
        self.tick = tick
        self.domain = domain
        self.props = kwargs

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "angle": self.angle,
                "type": self.type,
                "tick": self.tick,
                "domain": self.domain,
                **self.props,
            },
        }
