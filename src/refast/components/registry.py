"""Component registry for custom React components."""

from dataclasses import dataclass
from typing import Any

from refast.components.base import Component


@dataclass
class ComponentRegistration:
    """Registration info for a custom component."""

    name: str
    component_class: type[Component]
    package: str | None = None
    module: str | None = None


_registry: dict[str, ComponentRegistration] = {}


def register_component(
    name: str,
    package: str | None = None,
    module: str | None = None,
):
    """
    Decorator to register a custom React component.

    Args:
        name: The React component name
        package: NPM package containing the component
        module: Export name from the package

    Example:
        ```python
        @register_component(
            name="Chart",
            package="refast-chartjs",
            module="Chart"
        )
        class Chart(Component):
            ...
        ```
    """

    def decorator(cls: type[Component]) -> type[Component]:
        cls.component_type = name
        _registry[name] = ComponentRegistration(
            name=name,
            component_class=cls,
            package=package,
            module=module,
        )
        return cls

    return decorator


def get_component(name: str) -> ComponentRegistration | None:
    """Get a registered component by name."""
    return _registry.get(name)


def list_components() -> list[str]:
    """List all registered component names."""
    return list(_registry.keys())


def get_component_packages() -> dict[str, str]:
    """Get mapping of component names to packages."""
    return {name: reg.package for name, reg in _registry.items() if reg.package}


def clear_registry() -> None:
    """Clear the component registry. Useful for testing."""
    _registry.clear()


class ReactComponent(Component):
    """
    Base class for wrapping external React components.

    Use this when wrapping a React component from an external package.

    Example:
        ```python
        @register_component("MyChart", package="my-charts", module="Chart")
        class MyChart(ReactComponent):
            def __init__(self, data: list, on_click: Callback = None):
                super().__init__(
                    props={"data": data},
                    events={"onClick": on_click}
                )
        ```
    """

    def __init__(
        self,
        props: dict[str, Any] | None = None,
        events: dict[str, Any] | None = None,
        id: str | None = None,
        class_name: str = "",
    ):
        super().__init__(id=id, class_name=class_name)
        self._props = props or {}
        self._events = events or {}

    def render(self) -> dict[str, Any]:
        # Serialize events
        serialized_events = {}
        for event_name, callback in self._events.items():
            if callback is not None:
                if hasattr(callback, "serialize"):
                    serialized_events[event_name] = callback.serialize()
                else:
                    serialized_events[event_name] = callback

        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                **self._props,
                **serialized_events,
                "className": self.class_name,
            },
            "children": self._render_children(),
        }
