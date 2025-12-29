# Stage 2: Component System

## Progress

- [x] Task 2.1: Base component classes
- [x] Task 2.2: Component registry
- [x] Task 2.3: Slot component
- [x] Task 2.4: Layout components
- [x] Task 2.5: Input components
- [x] Task 2.6: Feedback components
- [x] Task 2.7: Data display components

## Objectives

Build the component system that allows defining UI in Python:
- Base `Component` class with rendering logic
- Component registry for custom components
- Default shadcn-based components
- Layout, input, feedback, and data display components

## Prerequisites

- Stage 1 complete
- Understanding of React component structure

---

## Task 2.1: Base Component Classes

### Description
Create the foundational component classes that all components inherit from.

### Files to Create

**src/refast/components/__init__.py**
```python
"""Refast component system."""

from refast.components.base import Component, Container, Text, Fragment
from refast.components.slot import Slot
from refast.components.registry import register_component, get_component

# Re-export shadcn components
from refast.components.shadcn import (
    Button,
    Card,
    Input,
    Form,
    Row,
    Column,
    Stack,
    Heading,
    # ... more exports
)

__all__ = [
    "Component",
    "Container",
    "Text",
    "Fragment",
    "Slot",
    "register_component",
    "get_component",
    "Button",
    "Card",
    "Input",
    "Form",
    "Row",
    "Column",
    "Stack",
    "Heading",
]
```

**src/refast/components/base.py**
```python
"""Base component classes."""

from typing import Any, Self
from abc import ABC, abstractmethod
import uuid


class Component(ABC):
    """
    Base class for all Refast components.
    
    Components are Python objects that render to a dictionary structure
    that the frontend can interpret and render as React components.
    
    Example:
        ```python
        class MyButton(Component):
            component_type = "Button"
            
            def __init__(self, label: str, on_click: Callback | None = None):
                super().__init__()
                self.label = label
                self.on_click = on_click
            
            def render(self) -> dict[str, Any]:
                return {
                    "type": self.component_type,
                    "id": self.id,
                    "props": {"label": self.label},
                    "children": [],
                }
        ```
    """
    
    component_type: str = "Component"
    
    def __init__(
        self,
        id: str | None = None,
        class_name: str = "",
        style: dict[str, Any] | None = None,
        **props: Any,
    ):
        self.id = id or str(uuid.uuid4())
        self.class_name = class_name
        self.style = style or {}
        self.extra_props = props
        self._children: list["Component | str"] = []
    
    def add_child(self, child: "Component | str") -> Self:
        """Add a child component."""
        self._children.append(child)
        return self
    
    def add_children(self, children: list["Component | str"]) -> Self:
        """Add multiple children."""
        self._children.extend(children)
        return self
    
    def _render_children(self) -> list[dict[str, Any] | str]:
        """Render all children to dicts."""
        result = []
        for child in self._children:
            if isinstance(child, Component):
                result.append(child.render())
            else:
                result.append(str(child))
        return result
    
    @abstractmethod
    def render(self) -> dict[str, Any]:
        """
        Render the component to a dictionary.
        
        Returns:
            Dictionary with type, id, props, and children
        """
        pass
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r})"


class Container(Component):
    """
    Generic container component.
    
    Example:
        ```python
        Container(
            id="main",
            class_name="p-4",
            children=[
                Text("Hello"),
                Button("Click me"),
            ]
        )
        ```
    """
    
    component_type: str = "Container"
    
    def __init__(
        self,
        children: list["Component | str"] | None = None,
        id: str | None = None,
        class_name: str = "",
        style: dict[str, Any] | None = None,
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, style=style, **props)
        if children:
            self._children = children
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "className": self.class_name,
                "style": self.style,
                **self.extra_props,
            },
            "children": self._render_children(),
        }


class Text(Component):
    """
    Text component for displaying text content.
    
    Example:
        ```python
        Text("Hello, World!", class_name="text-lg font-bold")
        ```
    """
    
    component_type: str = "Text"
    
    def __init__(
        self,
        content: str,
        id: str | None = None,
        class_name: str = "",
        style: dict[str, Any] | None = None,
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, style=style, **props)
        self.content = content
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "className": self.class_name,
                "style": self.style,
                **self.extra_props,
            },
            "children": [self.content],
        }


class Fragment(Component):
    """
    Fragment component for grouping without a wrapper element.
    
    Example:
        ```python
        Fragment([
            Text("Line 1"),
            Text("Line 2"),
        ])
        ```
    """
    
    component_type: str = "Fragment"
    
    def __init__(self, children: list["Component | str"] | None = None):
        super().__init__()
        if children:
            self._children = children
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {},
            "children": self._render_children(),
        }
```

### Tests to Write

**tests/unit/test_components.py**
```python
import pytest
from refast.components.base import Component, Container, Text, Fragment

class TestComponent:
    def test_component_has_id(self):
        container = Container()
        assert container.id is not None
    
    def test_component_custom_id(self):
        container = Container(id="my-id")
        assert container.id == "my-id"
    
    def test_container_with_children(self):
        container = Container(children=[
            Text("Hello"),
            Text("World"),
        ])
        rendered = container.render()
        assert len(rendered["children"]) == 2
    
    def test_text_renders_content(self):
        text = Text("Hello")
        rendered = text.render()
        assert rendered["children"] == ["Hello"]
        assert rendered["type"] == "Text"
    
    def test_fragment_has_no_props(self):
        fragment = Fragment([Text("A")])
        rendered = fragment.render()
        assert rendered["props"] == {}
    
    def test_add_child_fluent(self):
        container = Container()
        result = container.add_child(Text("A")).add_child(Text("B"))
        assert result is container
        assert len(container._children) == 2
```

### Acceptance Criteria

- [ ] Base Component class works
- [ ] Container renders children
- [ ] Text renders content
- [ ] Fragment groups without wrapper
- [ ] Components have unique IDs

---

## Task 2.2: Component Registry

### Description
Create a registry for custom React components.

### Files to Create

**src/refast/components/registry.py**
```python
"""Component registry for custom React components."""

from typing import Any, Type
from dataclasses import dataclass

from refast.components.base import Component


@dataclass
class ComponentRegistration:
    """Registration info for a custom component."""
    name: str
    component_class: Type[Component]
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
    def decorator(cls: Type[Component]) -> Type[Component]:
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
    return {
        name: reg.package
        for name, reg in _registry.items()
        if reg.package
    }


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
```

### Tests to Write

**tests/unit/test_registry.py**
```python
import pytest
from refast.components.registry import (
    register_component,
    get_component,
    list_components,
    ReactComponent,
)
from refast.components.base import Component

class TestRegistry:
    def test_register_component(self):
        @register_component("TestComp", package="test-pkg")
        class TestComp(Component):
            def render(self):
                return {"type": "TestComp", "id": self.id, "props": {}, "children": []}
        
        reg = get_component("TestComp")
        assert reg is not None
        assert reg.package == "test-pkg"
    
    def test_list_components(self):
        names = list_components()
        assert isinstance(names, list)
    
    def test_react_component_renders(self):
        class MyComp(ReactComponent):
            component_type = "MyComp"
        
        comp = MyComp(props={"value": 42})
        rendered = comp.render()
        assert rendered["props"]["value"] == 42
```

### Acceptance Criteria

- [ ] Components can be registered
- [ ] Registry tracks package info
- [ ] ReactComponent base class works

---

## Task 2.3: Slot Component

### Description
Create the Slot component for placeholder content.

### Files to Create

**src/refast/components/slot.py**
```python
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
                "className": self.class_name,
                **self.extra_props,
            },
            "children": children,
        }
```

### Tests to Write

**tests/unit/test_slot.py**
```python
import pytest
from refast.components.slot import Slot
from refast.components.base import Text

class TestSlot:
    def test_slot_renders_children(self):
        slot = Slot(id="my-slot", children=[Text("Content")])
        rendered = slot.render()
        assert rendered["id"] == "my-slot"
        assert len(rendered["children"]) == 1
    
    def test_slot_with_fallback(self):
        slot = Slot(id="my-slot", fallback=Text("Loading..."))
        rendered = slot.render()
        assert len(rendered["children"]) == 1
    
    def test_slot_children_override_fallback(self):
        slot = Slot(
            id="my-slot",
            children=[Text("Actual")],
            fallback=Text("Fallback")
        )
        rendered = slot.render()
        assert rendered["children"][0]["children"] == ["Actual"]
```

### Acceptance Criteria

- [ ] Slot renders with ID
- [ ] Fallback works when no children
- [ ] Children override fallback

---

## Task 2.4: Layout Components

### Description
Create layout components (Row, Column, Stack, Grid, etc.)

### Files to Create

**src/refast/components/shadcn/__init__.py**
```python
"""shadcn-based components."""

from refast.components.shadcn.layout import (
    Row,
    Column,
    Stack,
    Grid,
    Flex,
    Center,
    Spacer,
    Divider,
)
from refast.components.shadcn.button import Button, IconButton
from refast.components.shadcn.card import Card, CardHeader, CardContent, CardFooter
from refast.components.shadcn.input import Input, Textarea, Select, Checkbox, Radio
from refast.components.shadcn.form import Form, FormField, Label
from refast.components.shadcn.feedback import (
    Alert,
    Toast,
    Modal,
    Dialog,
    Spinner,
    Progress,
    Skeleton,
)
from refast.components.shadcn.data_display import (
    Table,
    DataTable,
    List,
    Badge,
    Avatar,
    Tooltip,
    Tabs,
    TabItem,
    Accordion,
)
from refast.components.shadcn.typography import Heading, Paragraph, Code, Link

__all__ = [
    # Layout
    "Row", "Column", "Stack", "Grid", "Flex", "Center", "Spacer", "Divider",
    # Button
    "Button", "IconButton",
    # Card
    "Card", "CardHeader", "CardContent", "CardFooter",
    # Input
    "Input", "Textarea", "Select", "Checkbox", "Radio",
    # Form
    "Form", "FormField", "Label",
    # Feedback
    "Alert", "Toast", "Modal", "Dialog", "Spinner", "Progress", "Skeleton",
    # Data Display
    "Table", "DataTable", "List", "Badge", "Avatar", "Tooltip",
    "Tabs", "TabItem", "Accordion",
    # Typography
    "Heading", "Paragraph", "Code", "Link",
]
```

**src/refast/components/shadcn/layout.py**
```python
"""Layout components based on shadcn."""

from typing import Any, Literal
from refast.components.base import Component


class Row(Component):
    """
    Horizontal flex container.
    
    Example:
        ```python
        Row(
            children=[Button("A"), Button("B")],
            justify="between",
            align="center",
            gap=4,
        )
        ```
    """
    
    component_type: str = "Row"
    
    def __init__(
        self,
        children: list[Component | str] | None = None,
        justify: Literal["start", "end", "center", "between", "around", "evenly"] = "start",
        align: Literal["start", "end", "center", "stretch", "baseline"] = "start",
        gap: int | str = 0,
        wrap: bool = False,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children
        self.justify = justify
        self.align = align
        self.gap = gap
        self.wrap = wrap
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "justify": self.justify,
                "align": self.align,
                "gap": self.gap,
                "wrap": self.wrap,
                "className": self.class_name,
                **self.extra_props,
            },
            "children": self._render_children(),
        }


class Column(Component):
    """
    Vertical flex container.
    
    Example:
        ```python
        Column(
            children=[Text("Line 1"), Text("Line 2")],
            gap=2,
        )
        ```
    """
    
    component_type: str = "Column"
    
    def __init__(
        self,
        children: list[Component | str] | None = None,
        justify: Literal["start", "end", "center", "between", "around", "evenly"] = "start",
        align: Literal["start", "end", "center", "stretch", "baseline"] = "stretch",
        gap: int | str = 0,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children
        self.justify = justify
        self.align = align
        self.gap = gap
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "justify": self.justify,
                "align": self.align,
                "gap": self.gap,
                "className": self.class_name,
                **self.extra_props,
            },
            "children": self._render_children(),
        }


class Stack(Component):
    """
    Stack container with consistent spacing.
    
    Similar to Column but with simpler API for common use cases.
    """
    
    component_type: str = "Stack"
    
    def __init__(
        self,
        children: list[Component | str] | None = None,
        spacing: int | str = 4,
        direction: Literal["vertical", "horizontal"] = "vertical",
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children
        self.spacing = spacing
        self.direction = direction
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "spacing": self.spacing,
                "direction": self.direction,
                "className": self.class_name,
                **self.extra_props,
            },
            "children": self._render_children(),
        }


class Grid(Component):
    """
    CSS Grid container.
    
    Example:
        ```python
        Grid(
            children=[Card(...) for _ in range(6)],
            columns=3,
            gap=4,
        )
        ```
    """
    
    component_type: str = "Grid"
    
    def __init__(
        self,
        children: list[Component | str] | None = None,
        columns: int | str = 1,
        rows: int | str | None = None,
        gap: int | str = 0,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children
        self.columns = columns
        self.rows = rows
        self.gap = gap
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "columns": self.columns,
                "rows": self.rows,
                "gap": self.gap,
                "className": self.class_name,
                **self.extra_props,
            },
            "children": self._render_children(),
        }


class Flex(Component):
    """Generic flexbox container with full control."""
    
    component_type: str = "Flex"
    
    def __init__(
        self,
        children: list[Component | str] | None = None,
        direction: Literal["row", "column", "row-reverse", "column-reverse"] = "row",
        justify: str = "start",
        align: str = "stretch",
        wrap: Literal["nowrap", "wrap", "wrap-reverse"] = "nowrap",
        gap: int | str = 0,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children
        self.direction = direction
        self.justify = justify
        self.align = align
        self.wrap = wrap
        self.gap = gap
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "direction": self.direction,
                "justify": self.justify,
                "align": self.align,
                "wrap": self.wrap,
                "gap": self.gap,
                "className": self.class_name,
                **self.extra_props,
            },
            "children": self._render_children(),
        }


class Center(Component):
    """Center content horizontally and vertically."""
    
    component_type: str = "Center"
    
    def __init__(
        self,
        children: list[Component | str] | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "className": self.class_name,
                **self.extra_props,
            },
            "children": self._render_children(),
        }


class Spacer(Component):
    """Flexible spacer that expands to fill available space."""
    
    component_type: str = "Spacer"
    
    def __init__(self, size: int | str | None = None, **props: Any):
        super().__init__(**props)
        self.size = size
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {"size": self.size, **self.extra_props},
            "children": [],
        }


class Divider(Component):
    """Horizontal or vertical divider line."""
    
    component_type: str = "Divider"
    
    def __init__(
        self,
        orientation: Literal["horizontal", "vertical"] = "horizontal",
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.orientation = orientation
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "orientation": self.orientation,
                "className": self.class_name,
                **self.extra_props,
            },
            "children": [],
        }
```

### Tests to Write

**tests/unit/test_layout.py**
```python
import pytest
from refast.components.shadcn.layout import Row, Column, Stack, Grid

class TestLayoutComponents:
    def test_row_renders(self):
        from refast.components.base import Text
        row = Row(children=[Text("A"), Text("B")], gap=4)
        rendered = row.render()
        assert rendered["type"] == "Row"
        assert rendered["props"]["gap"] == 4
        assert len(rendered["children"]) == 2
    
    def test_column_renders(self):
        col = Column(gap=2, justify="center")
        rendered = col.render()
        assert rendered["type"] == "Column"
        assert rendered["props"]["justify"] == "center"
    
    def test_stack_renders(self):
        stack = Stack(spacing=8, direction="horizontal")
        rendered = stack.render()
        assert rendered["type"] == "Stack"
        assert rendered["props"]["spacing"] == 8
    
    def test_grid_renders(self):
        grid = Grid(columns=3, gap=4)
        rendered = grid.render()
        assert rendered["type"] == "Grid"
        assert rendered["props"]["columns"] == 3
```

### Acceptance Criteria

- [ ] Row, Column, Stack work
- [ ] Grid component works
- [ ] Flex component works
- [ ] Center, Spacer, Divider work

---

## Task 2.5: Input Components

### Description
Create input components (Input, Textarea, Select, etc.)

### Files to Create

**src/refast/components/shadcn/input.py**
```python
"""Input components based on shadcn."""

from typing import Any, Literal
from refast.components.base import Component


class Input(Component):
    """
    Text input component.
    
    Example:
        ```python
        Input(
            name="email",
            label="Email Address",
            type="email",
            placeholder="you@example.com",
            on_change=ctx.callback(handle_change),
        )
        ```
    """
    
    component_type: str = "Input"
    
    def __init__(
        self,
        name: str,
        label: str | None = None,
        type: Literal["text", "email", "password", "number", "tel", "url", "search"] = "text",
        placeholder: str = "",
        value: str = "",
        required: bool = False,
        disabled: bool = False,
        readonly: bool = False,
        on_change: Any = None,
        on_blur: Any = None,
        on_focus: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.name = name
        self.label = label
        self.input_type = type
        self.placeholder = placeholder
        self.value = value
        self.required = required
        self.disabled = disabled
        self.readonly = readonly
        self.on_change = on_change
        self.on_blur = on_blur
        self.on_focus = on_focus
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "name": self.name,
                "label": self.label,
                "type": self.input_type,
                "placeholder": self.placeholder,
                "value": self.value,
                "required": self.required,
                "disabled": self.disabled,
                "readOnly": self.readonly,
                "onChange": self.on_change.serialize() if self.on_change else None,
                "onBlur": self.on_blur.serialize() if self.on_blur else None,
                "onFocus": self.on_focus.serialize() if self.on_focus else None,
                "className": self.class_name,
                **self.extra_props,
            },
            "children": [],
        }


class Textarea(Component):
    """Multi-line text input."""
    
    component_type: str = "Textarea"
    
    def __init__(
        self,
        name: str,
        label: str | None = None,
        placeholder: str = "",
        value: str = "",
        rows: int = 3,
        required: bool = False,
        disabled: bool = False,
        on_change: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.name = name
        self.label = label
        self.placeholder = placeholder
        self.value = value
        self.rows = rows
        self.required = required
        self.disabled = disabled
        self.on_change = on_change
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "name": self.name,
                "label": self.label,
                "placeholder": self.placeholder,
                "value": self.value,
                "rows": self.rows,
                "required": self.required,
                "disabled": self.disabled,
                "onChange": self.on_change.serialize() if self.on_change else None,
                "className": self.class_name,
                **self.extra_props,
            },
            "children": [],
        }


class Select(Component):
    """Dropdown select component."""
    
    component_type: str = "Select"
    
    def __init__(
        self,
        name: str,
        options: list[dict[str, str]],  # [{"value": "a", "label": "Option A"}, ...]
        label: str | None = None,
        value: str = "",
        placeholder: str = "Select...",
        required: bool = False,
        disabled: bool = False,
        on_change: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.name = name
        self.options = options
        self.label = label
        self.value = value
        self.placeholder = placeholder
        self.required = required
        self.disabled = disabled
        self.on_change = on_change
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "name": self.name,
                "options": self.options,
                "label": self.label,
                "value": self.value,
                "placeholder": self.placeholder,
                "required": self.required,
                "disabled": self.disabled,
                "onChange": self.on_change.serialize() if self.on_change else None,
                "className": self.class_name,
                **self.extra_props,
            },
            "children": [],
        }


class Checkbox(Component):
    """Checkbox input component."""
    
    component_type: str = "Checkbox"
    
    def __init__(
        self,
        name: str | None = None,
        label: str | None = None,
        checked: bool = False,
        disabled: bool = False,
        on_change: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.name = name
        self.label = label
        self.checked = checked
        self.disabled = disabled
        self.on_change = on_change
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "name": self.name,
                "label": self.label,
                "checked": self.checked,
                "disabled": self.disabled,
                "onChange": self.on_change.serialize() if self.on_change else None,
                "className": self.class_name,
                **self.extra_props,
            },
            "children": [],
        }


class Radio(Component):
    """Radio button component."""
    
    component_type: str = "Radio"
    
    def __init__(
        self,
        name: str,
        value: str,
        label: str | None = None,
        checked: bool = False,
        disabled: bool = False,
        on_change: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.name = name
        self.value = value
        self.label = label
        self.checked = checked
        self.disabled = disabled
        self.on_change = on_change
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "name": self.name,
                "value": self.value,
                "label": self.label,
                "checked": self.checked,
                "disabled": self.disabled,
                "onChange": self.on_change.serialize() if self.on_change else None,
                "className": self.class_name,
                **self.extra_props,
            },
            "children": [],
        }
```

### Acceptance Criteria

- [ ] Input component works
- [ ] Textarea component works
- [ ] Select component works
- [ ] Checkbox and Radio work
- [ ] All support on_change callback

---

## Task 2.6: Create Button and Card Components

### Files to Create

**src/refast/components/shadcn/button.py**
```python
"""Button components."""

from typing import Any, Literal
from refast.components.base import Component


class Button(Component):
    """
    Button component based on shadcn.
    
    Example:
        ```python
        Button(
            "Click Me",
            variant="primary",
            on_click=ctx.callback(handle_click)
        )
        ```
    """
    
    component_type: str = "Button"
    
    def __init__(
        self,
        label: str,
        variant: Literal["default", "primary", "secondary", "destructive", "outline", "ghost", "link"] = "default",
        size: Literal["sm", "md", "lg", "icon"] = "md",
        disabled: bool = False,
        loading: bool = False,
        type: Literal["button", "submit", "reset"] = "button",
        on_click: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.label = label
        self.variant = variant
        self.size = size
        self.disabled = disabled
        self.loading = loading
        self.button_type = type
        self.on_click = on_click
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "variant": self.variant,
                "size": self.size,
                "disabled": self.disabled or self.loading,
                "loading": self.loading,
                "type": self.button_type,
                "onClick": self.on_click.serialize() if self.on_click else None,
                "className": self.class_name,
                **self.extra_props,
            },
            "children": [self.label],
        }


class IconButton(Component):
    """Button with just an icon."""
    
    component_type: str = "IconButton"
    
    def __init__(
        self,
        icon: str,
        variant: Literal["default", "primary", "secondary", "destructive", "outline", "ghost"] = "ghost",
        size: Literal["sm", "md", "lg"] = "md",
        disabled: bool = False,
        on_click: Any = None,
        aria_label: str | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.icon = icon
        self.variant = variant
        self.size = size
        self.disabled = disabled
        self.on_click = on_click
        self.aria_label = aria_label
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "icon": self.icon,
                "variant": self.variant,
                "size": self.size,
                "disabled": self.disabled,
                "onClick": self.on_click.serialize() if self.on_click else None,
                "ariaLabel": self.aria_label,
                "className": self.class_name,
                **self.extra_props,
            },
            "children": [],
        }
```

**src/refast/components/shadcn/card.py**
```python
"""Card components."""

from typing import Any
from refast.components.base import Component


class Card(Component):
    """
    Card container component.
    
    Example:
        ```python
        Card(
            children=[
                CardHeader(title="My Card"),
                CardContent(children=[Text("Content here")]),
                CardFooter(children=[Button("Action")]),
            ]
        )
        ```
    """
    
    component_type: str = "Card"
    
    def __init__(
        self,
        children: list[Component | str] | None = None,
        title: str | None = None,
        description: str | None = None,
        on_click: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children
        self.title = title
        self.description = description
        self.on_click = on_click
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "title": self.title,
                "description": self.description,
                "onClick": self.on_click.serialize() if self.on_click else None,
                "className": self.class_name,
                **self.extra_props,
            },
            "children": self._render_children(),
        }


class CardHeader(Component):
    """Card header section."""
    
    component_type: str = "CardHeader"
    
    def __init__(
        self,
        title: str | None = None,
        description: str | None = None,
        children: list[Component | str] | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children
        self.title = title
        self.description = description
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "title": self.title,
                "description": self.description,
                "className": self.class_name,
                **self.extra_props,
            },
            "children": self._render_children(),
        }


class CardContent(Component):
    """Card content section."""
    
    component_type: str = "CardContent"
    
    def __init__(
        self,
        children: list[Component | str] | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "className": self.class_name,
                **self.extra_props,
            },
            "children": self._render_children(),
        }


class CardFooter(Component):
    """Card footer section."""
    
    component_type: str = "CardFooter"
    
    def __init__(
        self,
        children: list[Component | str] | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "className": self.class_name,
                **self.extra_props,
            },
            "children": self._render_children(),
        }
```

### Acceptance Criteria

- [ ] Button with variants works
- [ ] IconButton works
- [ ] Card with sections works

---

## Task 2.7: Create Remaining Components

Create the remaining component files (form, feedback, data_display, typography).

These follow the same patterns as above. See the full component list in the `__init__.py`.

---

## Final Checklist for Stage 2

- [ ] All component files created
- [ ] All components have render() methods
- [ ] All tests pass
- [ ] Components are exported correctly
- [ ] Update `.github/copilot-instructions.md` status to 🟢
