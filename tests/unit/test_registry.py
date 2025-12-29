"""Tests for component registry."""

import pytest

from refast.components.base import Component
from refast.components.registry import (
    ReactComponent,
    clear_registry,
    get_component,
    get_component_packages,
    list_components,
    register_component,
)


@pytest.fixture(autouse=True)
def clean_registry():
    """Clean registry before each test."""
    clear_registry()
    yield
    clear_registry()


class TestRegistry:
    """Tests for component registration."""

    def test_register_component(self):
        """Test registering a component."""

        @register_component("TestComp", package="test-pkg")
        class TestComp(Component):
            def render(self):
                return {"type": "TestComp", "id": self.id, "props": {}, "children": []}

        reg = get_component("TestComp")
        assert reg is not None
        assert reg.name == "TestComp"
        assert reg.package == "test-pkg"

    def test_register_component_with_module(self):
        """Test registering a component with module info."""

        @register_component("ChartComp", package="chart-lib", module="Chart")
        class ChartComp(Component):
            def render(self):
                return {"type": "ChartComp", "id": self.id, "props": {}, "children": []}

        reg = get_component("ChartComp")
        assert reg.module == "Chart"

    def test_get_component_not_found(self):
        """Test getting a non-existent component."""
        assert get_component("NonExistent") is None

    def test_list_components(self):
        """Test listing registered components."""

        @register_component("Comp1")
        class Comp1(Component):
            def render(self):
                return {}

        @register_component("Comp2")
        class Comp2(Component):
            def render(self):
                return {}

        names = list_components()
        assert "Comp1" in names
        assert "Comp2" in names

    def test_get_component_packages(self):
        """Test getting component packages."""

        @register_component("WithPkg", package="my-pkg")
        class WithPkg(Component):
            def render(self):
                return {}

        @register_component("NoPkg")
        class NoPkg(Component):
            def render(self):
                return {}

        packages = get_component_packages()
        assert "WithPkg" in packages
        assert packages["WithPkg"] == "my-pkg"
        assert "NoPkg" not in packages

    def test_register_sets_component_type(self):
        """Test that registration sets component_type."""

        @register_component("CustomType")
        class MyComp(Component):
            def render(self):
                return {"type": self.component_type}

        comp = MyComp()
        assert comp.component_type == "CustomType"


class TestReactComponent:
    """Tests for ReactComponent base class."""

    def test_react_component_renders(self):
        """Test ReactComponent renders props."""

        class MyComp(ReactComponent):
            component_type = "MyComp"

        comp = MyComp(props={"value": 42, "name": "test"})
        rendered = comp.render()
        assert rendered["props"]["value"] == 42
        assert rendered["props"]["name"] == "test"

    def test_react_component_with_events(self):
        """Test ReactComponent with events."""

        class ClickableComp(ReactComponent):
            component_type = "ClickableComp"

        # Mock callback with serialize method
        class MockCallback:
            def serialize(self):
                return {"callbackId": "cb-123"}

        comp = ClickableComp(events={"onClick": MockCallback()})
        rendered = comp.render()
        assert rendered["props"]["onClick"] == {"callbackId": "cb-123"}

    def test_react_component_with_class_name(self):
        """Test ReactComponent with class_name."""

        class StyledComp(ReactComponent):
            component_type = "StyledComp"

        comp = StyledComp(class_name="custom-class")
        rendered = comp.render()
        assert rendered["props"]["className"] == "custom-class"

    def test_react_component_none_events(self):
        """Test ReactComponent handles None events."""

        class OptionalComp(ReactComponent):
            component_type = "OptionalComp"

        comp = OptionalComp(events={"onClick": None})
        rendered = comp.render()
        assert "onClick" not in rendered["props"]
