"""Composed chart components for mixed chart types."""

from typing import Any, Literal

from refast.components.base import Component
from refast.events.types import Callback


class ComposedChart(Component):
    """
    Composed chart component for combining Bar, Line, and Area.

    Example:
        ```python
        ComposedChart(
            data=data,
            Bar(data_key="uv", fill="hsl(var(--chart-1))"),
            Line(data_key="pv", stroke="hsl(var(--chart-2))"),
            Area(data_key="amt", fill="hsl(var(--chart-3))"),
        )
        ```

    Args:
        data: List of data dictionaries
        margin: Chart margins
        layout: Chart layout direction
        bar_category_gap: Gap between bar categories
        bar_gap: Gap between bars in same category
        bar_size: Default bar size
        sync_id: ID for syncing multiple charts
        sync_method: How to sync charts
        on_click: Click event handler
        on_mouse_enter: Mouse enter handler
        on_mouse_leave: Mouse leave handler
        on_mouse_move: Mouse move handler
    """

    component_type: str = "ComposedChart"

    def __init__(
        self,
        *children: Component,
        data: list[dict[str, Any]],
        margin: dict[str, int] | None = None,
        layout: Literal["horizontal", "vertical"] = "horizontal",
        bar_category_gap: str | int | None = None,
        bar_gap: str | int | None = None,
        bar_size: int | None = None,
        sync_id: str | None = None,
        sync_method: Literal["index", "value"] | None = None,
        on_click: Callback | None = None,
        on_mouse_enter: Callback | None = None,
        on_mouse_leave: Callback | None = None,
        on_mouse_move: Callback | None = None,
        **kwargs: Any,
    ):
        kw_children = kwargs.pop("children", None)
        super().__init__(**kwargs)
        self.data = data
        self.margin = margin or {"top": 20, "right": 20, "left": 20, "bottom": 20}
        self.layout = layout
        self.bar_category_gap = bar_category_gap
        self.bar_gap = bar_gap
        self.bar_size = bar_size
        self.sync_id = sync_id
        self.sync_method = sync_method
        self.on_click = on_click
        self.on_mouse_enter = on_mouse_enter
        self.on_mouse_leave = on_mouse_leave
        self.on_mouse_move = on_mouse_move

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
                "layout": self.layout,
                "barCategoryGap": self.bar_category_gap,
                "barGap": self.bar_gap,
                "barSize": self.bar_size,
                "syncId": self.sync_id,
                "syncMethod": self.sync_method,
                "onClick": self.on_click.serialize() if self.on_click else None,
                "onMouseEnter": (self.on_mouse_enter.serialize() if self.on_mouse_enter else None),
                "onMouseLeave": (self.on_mouse_leave.serialize() if self.on_mouse_leave else None),
                "onMouseMove": (self.on_mouse_move.serialize() if self.on_mouse_move else None),
            },
            "children": [c.render() for c in self.children],
        }
