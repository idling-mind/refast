"""Sankey diagram component."""

from typing import Any

from refast.components.base import Component
from refast.events.types import Callback


class Sankey(Component):
    """
    Sankey diagram component for flow visualization.

    Example:
        ```python
        Sankey(
            data={
                "nodes": [
                    {"name": "Visit"},
                    {"name": "Direct-Aquisition"},
                    {"name": "Page-A"},
                    {"name": "Page-B"},
                    {"name": "Page-C"},
                    {"name": "Lost"},
                ],
                "links": [
                    {"source": 0, "target": 1, "value": 3728.3},
                    {"source": 0, "target": 2, "value": 354170},
                    {"source": 2, "target": 3, "value": 62429},
                    {"source": 2, "target": 4, "value": 291741},
                    {"source": 1, "target": 5, "value": 2006.1},
                ],
            },
            node_padding=10,
            node_width=10,
        )
        ```

    Args:
        data: Sankey data with 'nodes' and 'links' lists
        width: Width
        height: Height
        data_key: Key for link values
        name_key: Key for node names
        node_padding: Vertical padding between nodes
        node_width: Width of node rectangles
        link_curvature: Curvature of links (0-1)
        iterations: Number of layout iterations
        node: Node configuration
        link: Link configuration
        margin: Chart margins
        sort: Sort nodes
        on_click: Click event handler
        on_mouse_enter: Mouse enter handler
        on_mouse_leave: Mouse leave handler
    """

    component_type: str = "Sankey"

    def __init__(
        self,
        data: dict[str, Any],
        width: int | str = "100%",
        height: int | str = 400,
        data_key: str = "value",
        name_key: str = "name",
        node_padding: int = 10,
        node_width: int = 10,
        link_curvature: float = 0.5,
        iterations: int = 32,
        node: dict[str, Any] | None = None,
        link: dict[str, Any] | None = None,
        margin: dict[str, int] | None = None,
        sort: bool = True,
        on_click: Callback | None = None,
        on_mouse_enter: Callback | None = None,
        on_mouse_leave: Callback | None = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.data = data
        self.width = width
        self.height = height
        self.data_key = data_key
        self.name_key = name_key
        self.node_padding = node_padding
        self.node_width = node_width
        self.link_curvature = link_curvature
        self.iterations = iterations
        self.node = node
        self.link = link
        self.margin = margin or {"top": 10, "right": 10, "left": 10, "bottom": 10}
        self.sort = sort
        self.on_click = on_click
        self.on_mouse_enter = on_mouse_enter
        self.on_mouse_leave = on_mouse_leave
        self.extra_props = kwargs

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "data": self.data,
                "width": self.width,
                "height": self.height,
                "data_key": self.data_key,
                "name_key": self.name_key,
                "nodePadding": self.node_padding,
                "nodeWidth": self.node_width,
                "linkCurvature": self.link_curvature,
                "iterations": self.iterations,
                "node": self.node,
                "link": self.link,
                "margin": self.margin,
                "sort": self.sort,
                "on_click": self.on_click.serialize() if self.on_click else None,
                "on_mouse_enter": (
                    self.on_mouse_enter.serialize() if self.on_mouse_enter else None
                ),
                "on_mouse_leave": (
                    self.on_mouse_leave.serialize() if self.on_mouse_leave else None
                ),
                **self.extra_props,
            },
        }
