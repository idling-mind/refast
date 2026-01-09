"""Slot component for dynamic content placeholders."""

from typing import Any

from refast.components.base import Component


class Slot(Component):
    """
    Placeholder component that can be replaced dynamically.

    Slots are useful for content that will be loaded or replaced later.

    Example:
        ```python
        Container([
            Header("My App"),
            Slot(
                id="main-content",
                children=[Text("Loading...")]
            ),
        ])

        # Later, replace the slot
        await ctx.replace("main-content", ActualContent())
        ```
    """

    component_type: str = "Slot"

    def __init__(
        self,
        children: list[Component | str] | None = None,
        id: str | None = None,
        class_name: str = "",
        fallback: Component | None = None,
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children
        self.fallback = fallback

    def render(self) -> dict[str, Any]:
        children = self._render_children()
        if not children and self.fallback:
            children = [self.fallback.render()]

        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "class_name": self.class_name,
                **self.extra_props,
            },
            "children": children,
        }
