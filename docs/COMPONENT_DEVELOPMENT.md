# Refast Component Development Guide

This comprehensive guide explains how to create and register new components and component collections for the Refast framework. Components in Refast are Python classes that render to dictionaries, which the React frontend interprets and renders.

## Table of Contents

1. [Overview](#overview)
2. [Component Architecture](#component-architecture)
3. [Creating a Simple Component](#creating-a-simple-component)
4. [Creating a Component Collection](#creating-a-component-collection)
5. [Handling Events and Callbacks](#handling-events-and-callbacks)
6. [Creating the Frontend React Component](#creating-the-frontend-react-component)
7. [Registering Components](#registering-components)
8. [Testing Components](#testing-components)
9. [Best Practices](#best-practices)
10. [Complete Example: Rating Component](#complete-example-rating-component)

---

## Overview

Refast uses a two-layer component architecture:

1. **Python Components** (`src/refast/components/`): Define the component's API, props, and serialization to JSON
2. **React Components** (`src/refast-client/src/components/`): Render the actual UI in the browser

The flow is:
```
Python Component → render() → JSON → WebSocket → React ComponentRenderer → React Component → DOM
```

---

## Component Architecture

### Base Component Class

All components inherit from `Component` (in `src/refast/components/base.py`):

```python
from abc import ABC, abstractmethod
from typing import Any
import uuid

class Component(ABC):
    component_type: str = "Component"  # Maps to React component name
    
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
        self._children: list[Component | str] = []
    
    @abstractmethod
    def render(self) -> dict[str, Any]:
        """Render component to dictionary for frontend."""
        pass
```

### Key Methods

| Method | Description |
|--------|-------------|
| `render()` | **Required**. Returns dict with `type`, `id`, `props`, and `children` |
| `add_child(child)` | Add a single child, returns `self` for chaining |
| `add_children(children)` | Add multiple children at once |
| `_render_children()` | Helper to render all children to dicts/strings |
| `_serialize_extra_props()` | Helper to serialize extra props including callbacks |

---

## Creating a Simple Component

### Step 1: Create the Python Component

Create a new file in `src/refast/components/shadcn/` (or a custom folder for your collection):

```python
# src/refast/components/shadcn/rating.py
"""Rating component for star ratings."""

from typing import Any, Literal

from refast.components.base import Component


class Rating(Component):
    """
    Star rating component.
    
    Example:
        ```python
        Rating(
            value=3,
            max_stars=5,
            on_change=ctx.callback(handle_rating_change)
        )
        ```
    
    Args:
        value: Current rating value (0 to max_stars)
        max_stars: Maximum number of stars
        size: Size of the stars
        readonly: If True, rating cannot be changed
        on_change: Callback when rating changes
        id: Component ID
        class_name: CSS classes
    """
    
    component_type: str = "Rating"  # Must match React component name
    
    def __init__(
        self,
        value: int = 0,
        max_stars: int = 5,
        size: Literal["sm", "md", "lg"] = "md",
        readonly: bool = False,
        on_change: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.value = value
        self.max_stars = max_stars
        self.size = size
        self.readonly = readonly
        self.on_change = on_change
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "value": self.value,
                "maxStars": self.max_stars,  # camelCase for JS
                "size": self.size,
                "readonly": self.readonly,
                "onChange": self.on_change.serialize() if self.on_change else None,
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }
```

### Step 2: Export from the Module

Add to `src/refast/components/shadcn/__init__.py`:

```python
from refast.components.shadcn.rating import Rating

__all__ = [
    # ... existing exports ...
    "Rating",
]
```

### Step 3: Export from Main Components Module

Add to `src/refast/components/__init__.py`:

```python
from refast.components.shadcn import (
    # ... existing imports ...
    Rating,
)

__all__ = [
    # ... existing exports ...
    "Rating",
]
```

---

## Creating a Component Collection

Component collections group related components together. For example, the `Card` collection includes `Card`, `CardHeader`, `CardContent`, `CardFooter`, `CardTitle`, and `CardDescription`.

### Structure for a Collection

```
src/refast/components/shadcn/
└── my_collection.py  # Contains all related components
```

### Example: Stats Collection

```python
# src/refast/components/shadcn/stats.py
"""Stats display components."""

from typing import Any, Literal

from refast.components.base import Component


class StatCard(Component):
    """
    Card displaying a single statistic.
    
    Example:
        ```python
        StatCard(
            title="Total Users",
            value="12,345",
            change="+12.5%",
            trend="up",
            icon="users"
        )
        ```
    """
    
    component_type: str = "StatCard"
    
    def __init__(
        self,
        title: str,
        value: str | int | float,
        change: str | None = None,
        trend: Literal["up", "down", "neutral"] | None = None,
        icon: str | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.title = title
        self.value = value
        self.change = change
        self.trend = trend
        self.icon = icon
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "title": self.title,
                "value": str(self.value),
                "change": self.change,
                "trend": self.trend,
                "icon": self.icon,
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class StatGroup(Component):
    """
    Container for grouping multiple StatCards.
    
    Example:
        ```python
        StatGroup(
            columns=4,
            children=[
                StatCard(title="Users", value=1234),
                StatCard(title="Revenue", value="$12.3K"),
                StatCard(title="Orders", value=567),
                StatCard(title="Conversion", value="2.4%"),
            ]
        )
        ```
    """
    
    component_type: str = "StatGroup"
    
    def __init__(
        self,
        children: list[Component | str] | None = None,
        columns: int = 4,
        gap: int | str = 4,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children
        self.columns = columns
        self.gap = gap
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "columns": self.columns,
                "gap": self.gap,
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }
```

---

## Handling Events and Callbacks

### Callback Serialization

When a component accepts event handlers (like `on_click`, `on_change`), they must be serialized properly:

```python
def render(self) -> dict[str, Any]:
    return {
        "type": self.component_type,
        "id": self.id,
        "props": {
            # Always check if callback exists before serializing
            "onClick": self.on_click.serialize() if self.on_click else None,
            "onChange": self.on_change.serialize() if self.on_change else None,
            # ... other props
        },
        "children": self._render_children(),
    }
```

### Callback Object Structure

When serialized, a callback becomes:

```python
{
    "callbackId": "cb-uuid-string",
    "boundArgs": {"key": "value"},  # Optional bound arguments
    "debounce": 300,  # Optional debounce in ms
    "throttle": 100,  # Optional throttle in ms
}
```

### Using Callbacks in Apps

```python
from refast import Context, RefastApp
from refast.components import Rating

ui = RefastApp()

async def handle_rating_change(ctx: Context):
    """Handle rating change event."""
    new_rating = ctx.event_data.get("value")
    ctx.state.set("rating", new_rating)
    await ctx.push_update()

@ui.page("/")
def home(ctx: Context):
    return Rating(
        value=ctx.state.get("rating", 0),
        on_change=ctx.callback(handle_rating_change)
    )
```

---

## Creating the Frontend React Component

### Step 1: Create the React Component

Create the corresponding React component in `src/refast-client/src/components/shadcn/`:

```tsx
// src/refast-client/src/components/shadcn/rating.tsx
import React from 'react';
import { cn } from '../../utils';

interface RatingProps {
  id?: string;
  className?: string;
  value?: number;
  maxStars?: number;
  size?: 'sm' | 'md' | 'lg';
  readonly?: boolean;
  onChange?: (value: number) => void;
  'data-refast-id'?: string;
}

const sizeClasses = {
  sm: 'w-4 h-4',
  md: 'w-6 h-6',
  lg: 'w-8 h-8',
};

/**
 * Rating component - star rating input.
 */
export function Rating({
  id,
  className,
  value = 0,
  maxStars = 5,
  size = 'md',
  readonly = false,
  onChange,
  'data-refast-id': dataRefastId,
}: RatingProps): React.ReactElement {
  const [hoverValue, setHoverValue] = React.useState<number | null>(null);
  
  const handleClick = (starValue: number) => {
    if (!readonly && onChange) {
      onChange(starValue);
    }
  };
  
  const displayValue = hoverValue !== null ? hoverValue : value;
  
  return (
    <div
      id={id}
      className={cn('inline-flex gap-1', className)}
      data-refast-id={dataRefastId}
    >
      {Array.from({ length: maxStars }, (_, i) => i + 1).map((starValue) => (
        <button
          key={starValue}
          type="button"
          disabled={readonly}
          onClick={() => handleClick(starValue)}
          onMouseEnter={() => !readonly && setHoverValue(starValue)}
          onMouseLeave={() => setHoverValue(null)}
          className={cn(
            sizeClasses[size],
            'transition-colors',
            readonly ? 'cursor-default' : 'cursor-pointer',
            starValue <= displayValue
              ? 'text-yellow-400 fill-yellow-400'
              : 'text-gray-300'
          )}
        >
          <svg
            className="w-full h-full"
            viewBox="0 0 24 24"
            fill="currentColor"
            stroke="currentColor"
            strokeWidth="1"
          >
            <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
          </svg>
        </button>
      ))}
    </div>
  );
}
```

### Step 2: Export from shadcn Module

If you're creating a new file, add exports:

```tsx
// At the end of src/refast-client/src/components/shadcn/rating.tsx
export { Rating };
```

### Step 3: Register in Component Registry

Add to `src/refast-client/src/components/registry.ts`:

```typescript
// Import at the top
import { Rating } from './shadcn/rating';

// Register in the registry (near the end)
componentRegistry.register('Rating', Rating);
```

---

## Registering Components

### Python Side Registration

There are two ways to register components:

#### 1. Standard Registration (Built-in Components)

For components that are part of Refast core:

```python
# Add to src/refast/components/shadcn/__init__.py
from refast.components.shadcn.rating import Rating

# Add to src/refast/components/__init__.py  
from refast.components.shadcn import Rating
```

#### 2. Custom Component Registration (External Packages)

For components from external packages, use the `@register_component` decorator:

```python
from refast.components.registry import register_component, ReactComponent

@register_component(
    name="ChartJS",
    package="refast-chartjs",
    module="Chart"
)
class ChartJS(ReactComponent):
    """Chart.js component wrapper."""
    
    def __init__(
        self,
        chart_type: str,
        data: dict,
        options: dict | None = None,
        **kwargs
    ):
        super().__init__(
            props={
                "type": chart_type,
                "data": data,
                "options": options or {},
            },
            **kwargs
        )
```

### Frontend Side Registration

In `src/refast-client/src/components/registry.ts`:

```typescript
import { Rating } from './shadcn/rating';

// Register the component
componentRegistry.register('Rating', Rating);
```

The `ComponentRegistry` class provides these methods:

```typescript
class ComponentRegistry {
  register(name: string, component: ComponentType): void;
  get(name: string): ComponentType | undefined;
  has(name: string): boolean;
  list(): string[];
  registerAll(components: Record<string, ComponentType>): void;
}
```

---

## Testing Components

### Python Unit Tests

Create test file in `tests/unit/`:

```python
# tests/unit/test_rating.py
"""Tests for Rating component."""

import pytest
from refast.components.shadcn.rating import Rating


class MockCallback:
    """Mock callback for testing."""
    
    def serialize(self):
        return {"callbackId": "cb-123"}


class TestRating:
    """Tests for Rating component."""
    
    def test_rating_renders(self):
        """Test Rating renders correctly."""
        rating = Rating(value=3)
        rendered = rating.render()
        
        assert rendered["type"] == "Rating"
        assert rendered["props"]["value"] == 3
        assert rendered["props"]["maxStars"] == 5
    
    def test_rating_custom_max_stars(self):
        """Test Rating with custom max stars."""
        rating = Rating(value=7, max_stars=10)
        rendered = rating.render()
        
        assert rendered["props"]["maxStars"] == 10
    
    def test_rating_size(self):
        """Test Rating size prop."""
        rating = Rating(value=3, size="lg")
        rendered = rating.render()
        
        assert rendered["props"]["size"] == "lg"
    
    def test_rating_readonly(self):
        """Test Rating readonly prop."""
        rating = Rating(value=3, readonly=True)
        rendered = rating.render()
        
        assert rendered["props"]["readonly"] is True
    
    def test_rating_with_callback(self):
        """Test Rating with on_change callback."""
        cb = MockCallback()
        rating = Rating(value=3, on_change=cb)
        rendered = rating.render()
        
        assert rendered["props"]["onChange"] == {"callbackId": "cb-123"}
    
    def test_rating_without_callback(self):
        """Test Rating without callback renders None."""
        rating = Rating(value=3)
        rendered = rating.render()
        
        assert rendered["props"]["onChange"] is None
    
    def test_rating_class_name(self):
        """Test Rating accepts className."""
        rating = Rating(value=3, class_name="my-rating")
        rendered = rating.render()
        
        assert rendered["props"]["className"] == "my-rating"
    
    def test_rating_has_unique_id(self):
        """Test Rating generates unique ID."""
        r1 = Rating(value=1)
        r2 = Rating(value=2)
        
        assert r1.id != r2.id
    
    def test_rating_custom_id(self):
        """Test Rating accepts custom ID."""
        rating = Rating(value=3, id="my-rating")
        
        assert rating.id == "my-rating"
```

### Running Tests

```bash
# Run all tests
uv run pytest tests/

# Run specific test file
uv run pytest tests/unit/test_rating.py

# Run with coverage
uv run pytest tests/ --cov=src/refast --cov-report=html

# Run with verbose output
uv run pytest tests/unit/test_rating.py -v
```

---

## Best Practices

### 1. Naming Conventions

| Python | TypeScript/React | JSON Props |
|--------|------------------|------------|
| `class_name` | `className` | `className` |
| `on_click` | `onClick` | `onClick` |
| `max_stars` | `maxStars` | `maxStars` |
| `html_for` | `htmlFor` | `htmlFor` |

### 2. Type Hints

Always use complete type hints:

```python
from typing import Any, Literal

def __init__(
    self,
    value: int = 0,
    variant: Literal["default", "primary", "secondary"] = "default",
    on_change: Any = None,  # Callbacks use Any due to complex types
    id: str | None = None,
    class_name: str = "",
    **props: Any,
):
```

### 3. Documentation

Include comprehensive docstrings:

```python
class MyComponent(Component):
    """
    Brief description of the component.
    
    Example:
        ```python
        MyComponent(
            prop1="value",
            on_change=ctx.callback(handler)
        )
        ```
    
    Args:
        prop1: Description of prop1
        prop2: Description of prop2
        on_change: Callback when value changes
        id: Component ID
        class_name: Additional CSS classes
    """
```

### 4. Render Method Structure

Always follow this structure:

```python
def render(self) -> dict[str, Any]:
    return {
        "type": self.component_type,  # Required
        "id": self.id,                # Required
        "props": {
            # Component-specific props
            "myProp": self.my_prop,
            # Callbacks (always check for None)
            "onChange": self.on_change.serialize() if self.on_change else None,
            # Standard props
            "className": self.class_name,
            # Extra props (for flexibility)
            **self._serialize_extra_props(),
        },
        "children": self._render_children(),  # Required (can be empty list)
    }
```

### 5. Frontend Component Guidelines

```tsx
interface MyComponentProps {
  id?: string;
  className?: string;
  // Component-specific props
  myProp: string;
  // Event handlers
  onChange?: (value: string) => void;
  // Refast tracking
  'data-refast-id'?: string;
}

export function MyComponent({
  id,
  className,
  myProp,
  onChange,
  'data-refast-id': dataRefastId,
}: MyComponentProps): React.ReactElement {
  return (
    <div
      id={id}
      className={cn('base-classes', className)}
      data-refast-id={dataRefastId}
    >
      {/* Component content */}
    </div>
  );
}
```

### 6. Use Tailwind CSS

All styling should use Tailwind CSS utility classes:

```tsx
// Good
<div className="flex items-center gap-2 p-4 bg-card rounded-lg">

// Bad - Don't use inline styles
<div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
```

---

## Complete Example: Rating Component

Here's the complete implementation of a Rating component:

### Python Component

```python
# src/refast/components/shadcn/rating.py
"""Rating component for star ratings."""

from typing import Any, Literal

from refast.components.base import Component


class Rating(Component):
    """
    Star rating component for displaying and collecting ratings.
    
    Example:
        ```python
        # Read-only rating display
        Rating(value=4, readonly=True)
        
        # Interactive rating
        Rating(
            value=ctx.state.get("rating", 0),
            on_change=ctx.callback(handle_rating)
        )
        
        # Custom stars count
        Rating(value=7, max_stars=10, size="lg")
        ```
    
    Args:
        value: Current rating value (0 to max_stars)
        max_stars: Maximum number of stars (default: 5)
        size: Size of stars - "sm", "md", or "lg"
        readonly: If True, rating cannot be changed
        show_value: If True, show numeric value next to stars
        on_change: Callback when rating changes, receives new value
        id: Component ID
        class_name: Additional CSS classes
    """
    
    component_type: str = "Rating"
    
    def __init__(
        self,
        value: int = 0,
        max_stars: int = 5,
        size: Literal["sm", "md", "lg"] = "md",
        readonly: bool = False,
        show_value: bool = False,
        on_change: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.value = min(max(0, value), max_stars)  # Clamp value
        self.max_stars = max_stars
        self.size = size
        self.readonly = readonly
        self.show_value = show_value
        self.on_change = on_change
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "value": self.value,
                "maxStars": self.max_stars,
                "size": self.size,
                "readonly": self.readonly,
                "showValue": self.show_value,
                "onChange": self.on_change.serialize() if self.on_change else None,
                "className": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }
```

### React Component

```tsx
// src/refast-client/src/components/shadcn/rating.tsx
import React from 'react';
import { cn } from '../../utils';

interface RatingProps {
  id?: string;
  className?: string;
  value?: number;
  maxStars?: number;
  size?: 'sm' | 'md' | 'lg';
  readonly?: boolean;
  showValue?: boolean;
  onChange?: (value: number) => void;
  'data-refast-id'?: string;
}

const sizeClasses = {
  sm: 'w-4 h-4',
  md: 'w-6 h-6',
  lg: 'w-8 h-8',
};

const textSizeClasses = {
  sm: 'text-sm',
  md: 'text-base',
  lg: 'text-lg',
};

/**
 * Rating component - interactive star rating.
 */
export function Rating({
  id,
  className,
  value = 0,
  maxStars = 5,
  size = 'md',
  readonly = false,
  showValue = false,
  onChange,
  'data-refast-id': dataRefastId,
}: RatingProps): React.ReactElement {
  const [hoverValue, setHoverValue] = React.useState<number | null>(null);
  
  const handleClick = (starValue: number) => {
    if (!readonly && onChange) {
      // Toggle off if clicking the same value
      const newValue = starValue === value ? 0 : starValue;
      onChange(newValue);
    }
  };
  
  const displayValue = hoverValue !== null ? hoverValue : value;
  
  return (
    <div
      id={id}
      className={cn('inline-flex items-center gap-1', className)}
      data-refast-id={dataRefastId}
    >
      <div className="inline-flex gap-0.5">
        {Array.from({ length: maxStars }, (_, i) => i + 1).map((starValue) => {
          const isFilled = starValue <= displayValue;
          return (
            <button
              key={starValue}
              type="button"
              disabled={readonly}
              onClick={() => handleClick(starValue)}
              onMouseEnter={() => !readonly && setHoverValue(starValue)}
              onMouseLeave={() => setHoverValue(null)}
              className={cn(
                sizeClasses[size],
                'transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-ring rounded',
                readonly ? 'cursor-default' : 'cursor-pointer hover:scale-110',
                isFilled
                  ? 'text-yellow-400'
                  : 'text-muted-foreground/30'
              )}
              aria-label={`Rate ${starValue} out of ${maxStars}`}
            >
              <svg
                className="w-full h-full"
                viewBox="0 0 24 24"
                fill={isFilled ? 'currentColor' : 'none'}
                stroke="currentColor"
                strokeWidth="2"
              >
                <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
              </svg>
            </button>
          );
        })}
      </div>
      {showValue && (
        <span className={cn('ml-2 text-muted-foreground', textSizeClasses[size])}>
          {value}/{maxStars}
        </span>
      )}
    </div>
  );
}
```

### Unit Tests

```python
# tests/unit/test_rating.py
"""Tests for Rating component."""

import pytest
from refast.components.shadcn.rating import Rating


class MockCallback:
    """Mock callback for testing."""
    
    def serialize(self):
        return {"callbackId": "cb-test-123", "boundArgs": {}}


class TestRating:
    """Tests for Rating component."""
    
    def test_rating_default_values(self):
        """Test Rating with default values."""
        rating = Rating()
        rendered = rating.render()
        
        assert rendered["type"] == "Rating"
        assert rendered["props"]["value"] == 0
        assert rendered["props"]["maxStars"] == 5
        assert rendered["props"]["size"] == "md"
        assert rendered["props"]["readonly"] is False
        assert rendered["props"]["showValue"] is False
        assert rendered["props"]["onChange"] is None
    
    def test_rating_custom_values(self):
        """Test Rating with custom values."""
        rating = Rating(
            value=3,
            max_stars=10,
            size="lg",
            readonly=True,
            show_value=True,
        )
        rendered = rating.render()
        
        assert rendered["props"]["value"] == 3
        assert rendered["props"]["maxStars"] == 10
        assert rendered["props"]["size"] == "lg"
        assert rendered["props"]["readonly"] is True
        assert rendered["props"]["showValue"] is True
    
    def test_rating_value_clamped(self):
        """Test Rating value is clamped to valid range."""
        # Value too high
        rating = Rating(value=10, max_stars=5)
        assert rating.value == 5
        
        # Value too low
        rating = Rating(value=-5, max_stars=5)
        assert rating.value == 0
    
    def test_rating_with_callback(self):
        """Test Rating with callback."""
        cb = MockCallback()
        rating = Rating(value=3, on_change=cb)
        rendered = rating.render()
        
        assert rendered["props"]["onChange"]["callbackId"] == "cb-test-123"
    
    def test_rating_class_name(self):
        """Test Rating accepts class_name."""
        rating = Rating(class_name="custom-class")
        rendered = rating.render()
        
        assert rendered["props"]["className"] == "custom-class"
    
    def test_rating_extra_props(self):
        """Test Rating passes extra props."""
        rating = Rating(data_testid="rating-test")
        rendered = rating.render()
        
        assert "data_testid" in rendered["props"]
    
    def test_rating_unique_ids(self):
        """Test each Rating gets unique ID."""
        r1 = Rating()
        r2 = Rating()
        
        assert r1.id != r2.id
    
    def test_rating_custom_id(self):
        """Test Rating accepts custom ID."""
        rating = Rating(id="my-rating")
        
        assert rating.id == "my-rating"
        assert rating.render()["id"] == "my-rating"
```

### Usage Example

```python
# examples/rating_app/app.py
"""Rating component example."""

from fastapi import FastAPI
from refast import Context, RefastApp
from refast.components import (
    Card,
    CardContent,
    CardHeader,
    CardTitle,
    Column,
    Container,
    Rating,
    Row,
    Text,
)

ui = RefastApp(title="Rating Example")


async def handle_rating(ctx: Context):
    """Handle rating change."""
    new_rating = ctx.event_data.get("value", 0)
    ctx.state.set("user_rating", new_rating)
    await ctx.update_text("rating-text", f"You rated: {new_rating} stars")


@ui.page("/")
def home(ctx: Context):
    user_rating = ctx.state.get("user_rating", 0)
    
    return Container(
        class_name="max-w-md mx-auto mt-10",
        children=[
            Card(
                children=[
                    CardHeader(
                        children=[CardTitle("Rate Our Service")]
                    ),
                    CardContent(
                        children=[
                            Column(
                                gap=4,
                                children=[
                                    Text("How would you rate your experience?"),
                                    Rating(
                                        value=user_rating,
                                        size="lg",
                                        show_value=True,
                                        on_change=ctx.callback(handle_rating),
                                    ),
                                    Text(
                                        f"You rated: {user_rating} stars",
                                        id="rating-text",
                                        class_name="text-muted-foreground",
                                    ),
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )


# Create FastAPI app
app = FastAPI()
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## Summary

Creating a new component in Refast involves:

1. **Python Component** (`src/refast/components/shadcn/`)
   - Inherit from `Component`
   - Set `component_type` to match React component name
   - Implement `render()` returning proper dict structure
   - Export from `__init__.py` files

2. **React Component** (`src/refast-client/src/components/shadcn/`)
   - Create functional component with proper TypeScript interface
   - Use Tailwind CSS for styling
   - Include `data-refast-id` prop for tracking
   - Register in `registry.ts`

3. **Tests** (`tests/unit/`)
   - Test rendering, props, callbacks, and edge cases

4. **Documentation**
   - Include docstrings with examples
   - Document all props with types

Following these patterns ensures consistency across the component library and makes it easy for others to contribute new components.
