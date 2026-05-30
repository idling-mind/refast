"""Building Components — /docs/advanced/component-dev."""

from refast.components import Container, Heading, Markdown, Separator

PAGE_TITLE = "Building Components"
PAGE_ROUTE = "/docs/advanced/component-dev"


def render(ctx):
    """Render the component development guide page."""
    from docs_site.app import docs_layout

    content = Container(
        class_name="max-w-4xl mx-auto p-6",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            Markdown(content=CONTENT),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


CONTENT = r"""
Refast components are two-layer constructs: a **Python class** that defines props and
serializes to JSON, and a **React component** that renders the actual UI in the browser.
This guide walks through creating your own components from scratch.

## Architecture Overview

```
Python Component → render() → JSON dict → WebSocket → React ComponentRenderer → React Component → DOM
```

Every component has:

1. **Python side** — A class inheriting from `Component` with a `render()` method
2. **React side** — A functional component registered in `ComponentRegistry`

The frontend's `ComponentRenderer` receives the JSON and looks up the component by its
`type` field in the registry. Props are automatically converted from `snake_case` (Python)
to `camelCase` (React) by `ComponentRenderer`.

---

## Python Side

### Base Class

All components inherit from `Component` in `src/refast/components/base.py`:

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
        \"""Render component to dictionary for frontend.\"""
        pass
```

### Key Methods

| Method | Description |
|--------|-------------|
| `render()` | **Required.** Returns dict with `type`, `id`, `props`, and `children` |
| `add_children(children)` | Add multiple children at once |
| `_render_children()` | Helper to render all children to dicts/strings |
| `_serialize_extra_props()` | Helper to serialize extra props including callbacks |

### Common Props

Every component automatically gets these from the base class:

| Param | Type | Description |
|-------|------|-------------|
| `id` | `str \| None` | Component ID — auto-generated UUID if not provided |
| `class_name` | `str` | Tailwind CSS classes |
| `style` | `dict \| None` | Inline styles for truly dynamic values |
| `**props` | `Any` | Any additional props passed to the frontend |

### Implementing `render()`

The `render()` method must return a dictionary with this structure:

```python
def render(self) -> dict[str, Any]:
    return {
        "type": self.component_type,   # Required — matches React component name
        "id": self.id,                  # Required
        "props": {
            # Component-specific props in snake_case
            "value": self.value,
            "max_stars": self.max_stars,
            # Callbacks — always check for None before serializing
            "on_change": self.on_change.serialize() if self.on_change else None,
            # Standard props
            "class_name": self.class_name,
            # Pass through any extra props
            **self._serialize_extra_props(),
        },
        "children": self._render_children(),   # Required — can be empty list
    }
```

> **Important:** Always use `snake_case` for prop keys in `render()`. The frontend
> `ComponentRenderer` automatically converts them to `camelCase` for React.

### Children Rendering

Use `self._render_children()` to serialize child components:

```python
class MyContainer(Component):
    component_type: str = "MyContainer"

    def __init__(self, children=None, id=None, class_name="", **props):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children

    def render(self):
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {"class_name": self.class_name},
            "children": self._render_children(),   # Recursively renders children
        }
```

---

## Naming Conventions

Refast bridges two ecosystems with different naming conventions:

| Layer | Convention | Example |
|-------|------------|---------|
| Python `render()` props | `snake_case` | `on_click`, `class_name`, `max_value` |
| React component props | `camelCase` | `onClick`, `className`, `maxValue` |

The conversion happens in `ComponentRenderer.tsx` on the frontend:

```
Python render() emits  →  "on_click", "max_stars", "class_name"
ComponentRenderer converts →  "onClick",  "maxStars",  "className"
React component receives →  onClick,    maxStars,    className
```

**Correct:**

```python
def render(self) -> dict[str, Any]:
    return {
        "type": self.component_type,
        "id": self.id,
        "props": {
            "class_name": self.class_name,   # ✅ snake_case
            "on_click": self.on_click.serialize() if self.on_click else None,  # ✅
            "max_value": self.max_value,      # ✅
        },
        "children": self._render_children(),
    }
```

**Wrong:**

```python
def render(self) -> dict[str, Any]:
    return {
        "props": {
            "className": self.class_name,    # ❌ camelCase won't be converted
            "onClick": self.on_click,         # ❌
            "maxValue": self.max_value,       # ❌
        }
    }
```

This also applies to `ctx.update_props()` calls:

```python
# ✅ Correct
await ctx.update_props("my-id", {"foreground_color": "red", "is_disabled": True})

# ❌ Wrong
await ctx.update_props("my-id", {"foregroundColor": "red", "isDisabled": True})
```

### Development Validation

Enable prop validation during development to catch `camelCase` props early:

```bash
export REFAST_VALIDATE_PROPS=1   # Linux/Mac
$env:REFAST_VALIDATE_PROPS="1"  # PowerShell
```

This logs a warning whenever a component emits `camelCase` prop keys.

---

## Callback Props

When a component accepts event handlers like `on_click` or `on_change`, serialize them
with `.serialize()`:

```python
def render(self) -> dict[str, Any]:
    return {
        "type": self.component_type,
        "id": self.id,
        "props": {
            "on_click": self.on_click.serialize() if self.on_click else None,
            "on_change": self.on_change.serialize() if self.on_change else None,
        },
        "children": self._render_children(),
    }
```

A serialized callback looks like:

```json
{
  "callbackId": "cb-uuid-string",
  "boundArgs": {"key": "value"},
  "debounce": 300,
  "throttle": 100
}
```

### Using Callbacks in Apps

```python
from refast import Context, RefastApp

ui = RefastApp()

async def handle_rating_change(ctx: Context):
    new_rating = ctx.event_data.get("value")
    ctx.state.set("rating", new_rating)
    await ctx.refresh()

@ui.page("/")
def home(ctx: Context):
    return Rating(
        value=ctx.state.get("rating", 0),
        on_change=ctx.callback(handle_rating_change),
    )
```

### JavaScript Callbacks with `ctx.js()`

For interactions that don't require server-side processing, use `ctx.js()` to run
JavaScript directly in the browser — no WebSocket roundtrip:

```python
Button(
    "Toggle Theme",
    on_click=ctx.js("document.body.classList.toggle('dark')")
)
```

Available variables inside the JS string:

- **`event`** — event data object (`event.value`, `event.checked`, etc.)
- **`args`** — bound arguments passed to `ctx.js()`
- **`element`** — the DOM element that triggered the event

```python
Button(
    "Delete Item",
    on_click=ctx.js(
        "confirm('Delete ' + args.name + '?') && window.pendingDelete(args.id)",
        id=item["id"],
        name=item["name"],
    )
)
```

> **Security:** Never pass user-provided strings as the `code` argument. Use `args` for
> user data — they are serialized as JSON, not executed as code.

### Executing JavaScript from Python with `ctx.call_js()`

Call client-side JavaScript from within a Python callback:

```python
async def save_and_celebrate(ctx: Context):
    await database.save(ctx.event_data)
    await ctx.refresh()
    await ctx.call_js("confetti({ particleCount: 100 })")
    await ctx.call_js("window.scrollTo({ top: 0, behavior: 'smooth' })")
```

### Bound Component Methods

Some components expose imperative methods (e.g., a canvas's `clearCanvas()` or `undo()`).
Call them from Python using:

- **`ctx.bound_js("component-id", "methodName")`** — no server roundtrip, for event handlers
- **`ctx.call_bound_js("component-id", "methodName")`** — called from within a Python callback

```python
# Event handler — no server roundtrip
Button("Clear", on_click=ctx.bound_js("my-canvas", "clearCanvas"))
Button("Undo",  on_click=ctx.bound_js("my-canvas", "undo"))

# Inside a Python callback
async def load_drawing(ctx: Context):
    paths = await database.get_paths(ctx.event_data["id"])
    await ctx.call_bound_js("my-canvas", "loadPaths", paths=paths)
```

For a component to support these calls, its React wrapper must attach methods to the
DOM element — see the React side section below.

---

## React Side

### Creating the React Component

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
          onClick={() => !readonly && onChange && onChange(starValue)}
          onMouseEnter={() => !readonly && setHoverValue(starValue)}
          onMouseLeave={() => setHoverValue(null)}
          className={cn(
            sizeClasses[size],
            'transition-colors',
            readonly ? 'cursor-default' : 'cursor-pointer',
            starValue <= displayValue ? 'text-yellow-400' : 'text-muted-foreground/30',
          )}
        >
          ★
        </button>
      ))}
    </div>
  );
}
```

Key points:

- React props are `camelCase` — they arrive already converted from `snake_case`
- Always accept `'data-refast-id'` and forward it to the root element
- Use `id` on the **root** element so `ctx.bound_js()` can locate the component
- Use `cn()` (from `utils`) for combining Tailwind classes

### Registering in ComponentRegistry

Add the component to `src/refast-client/src/components/registry.ts`:

```typescript
import { Rating } from './shadcn/rating';

componentRegistry.register('Rating', Rating);
```

The registry API:

```typescript
componentRegistry.register(name: string, component: ComponentType): void
componentRegistry.get(name: string): ComponentType | undefined
componentRegistry.has(name: string): boolean
componentRegistry.list(): string[]
```

### Exposing Component Methods (for `ctx.bound_js()`)

Attach methods to the wrapper DOM element in a `useEffect` hook:

```tsx
import React, { useRef, useEffect } from 'react';

export function MyComponent({ id, className, 'data-refast-id': dataRefastId }) {
  const wrapperRef = useRef<HTMLDivElement>(null);

  const clear = () => { /* ... */ };
  const reset = () => { /* ... */ };

  useEffect(() => {
    const wrapper = wrapperRef.current;
    if (wrapper) {
      (wrapper as any).clear = clear;
      (wrapper as any).reset = reset;
    }
    return () => {
      if (wrapper) {
        delete (wrapper as any).clear;
        delete (wrapper as any).reset;
      }
    };
  });

  return (
    <div ref={wrapperRef} id={id} className={className} data-refast-id={dataRefastId}>
      {/* content */}
    </div>
  );
}
```

> **Important:** The `id` must be on the same element that has the methods attached.
> This is how `ctx.bound_js()` finds and calls them.

---

## Step-by-Step Walkthrough: Rating Component

### Step 1 — Python Component

```python
# src/refast/components/shadcn/rating.py
\"""Rating component for star ratings.\"""

from typing import Any, Literal
from refast.components.base import Component


class Rating(Component):
    \"""
    Star rating component.

    Example:
        ```python
        Rating(
            value=ctx.state.get("rating", 0),
            on_change=ctx.callback(handle_rating),
        )
        ```

    Args:
        value: Current rating (0 to max_stars)
        max_stars: Maximum number of stars (default: 5)
        size: Star size — "sm", "md", or "lg"
        readonly: If True, rating cannot be changed
        show_value: Show numeric value next to stars
        on_change: Callback when rating changes
        id: Component ID
        class_name: Additional CSS classes
    \"""

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
        self.value = min(max(0, value), max_stars)   # clamp to valid range
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
                "max_stars": self.max_stars,
                "size": self.size,
                "readonly": self.readonly,
                "show_value": self.show_value,
                "on_change": self.on_change.serialize() if self.on_change else None,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }
```

### Step 2 — Export from Module

```python
# src/refast/components/shadcn/__init__.py
from refast.components.shadcn.rating import Rating
```

```python
# src/refast/components/__init__.py
from refast.components.shadcn import Rating
```

### Step 3 — React Component (`rating.tsx`)

See the React example above. Add exports at the end:

```tsx
export { Rating };
```

### Step 4 — Register in `registry.ts`

```typescript
import { Rating } from './shadcn/rating';
componentRegistry.register('Rating', Rating);
```

### Step 5 — Use in an App

```python
from refast import Context, RefastApp
from refast.components import Card, CardContent, CardHeader, CardTitle, Column, Rating, Text

ui = RefastApp(title="Rating Example")

async def handle_rating(ctx: Context):
    new_rating = ctx.event_data.get("value", 0)
    ctx.state.set("user_rating", new_rating)
    await ctx.update_text("rating-display", f"You rated: {new_rating} stars")

@ui.page("/")
def home(ctx: Context):
    user_rating = ctx.state.get("user_rating", 0)
    return Card(
        children=[
            CardHeader(children=[CardTitle("Rate Our Service")]),
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
                                id="rating-display",
                                class_name="text-muted-foreground",
                            ),
                        ],
                    )
                ]
            ),
        ]
    )
```

---

## Component Collections

Group related components in a single file. For example, `Card` ships with
`CardHeader`, `CardContent`, `CardFooter`, `CardTitle`, and `CardDescription`
all in `card.py`.

```
src/refast/components/shadcn/
└── stats.py   # StatCard, StatGroup, etc.
```

```python
# src/refast/components/shadcn/stats.py

class StatCard(Component):
    component_type: str = "StatCard"

    def __init__(self, title: str, value: str | int | float,
                 change: str | None = None, trend: str | None = None,
                 id=None, class_name="", **props):
        super().__init__(id=id, class_name=class_name, **props)
        self.title = title
        self.value = value
        self.change = change
        self.trend = trend

    def render(self):
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "title": self.title,
                "value": str(self.value),
                "change": self.change,
                "trend": self.trend,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }
```

---

## Testing

### Python Unit Tests

```python
# tests/unit/test_rating.py
import pytest
from refast.components.shadcn.rating import Rating


class MockCallback:
    def serialize(self):
        return {"callbackId": "cb-123"}


class TestRating:
    def test_default_values(self):
        r = Rating()
        rendered = r.render()
        assert rendered["type"] == "Rating"
        assert rendered["props"]["value"] == 0
        assert rendered["props"]["max_stars"] == 5
        assert rendered["props"]["on_change"] is None

    def test_custom_values(self):
        r = Rating(value=3, max_stars=10, size="lg", readonly=True)
        rendered = r.render()
        assert rendered["props"]["value"] == 3
        assert rendered["props"]["max_stars"] == 10
        assert rendered["props"]["size"] == "lg"
        assert rendered["props"]["readonly"] is True

    def test_value_clamped(self):
        assert Rating(value=10, max_stars=5).value == 5
        assert Rating(value=-1).value == 0

    def test_callback_serialized(self):
        cb = MockCallback()
        rendered = Rating(value=3, on_change=cb).render()
        assert rendered["props"]["on_change"]["callbackId"] == "cb-123"

    def test_unique_ids(self):
        assert Rating().id != Rating().id

    def test_custom_id(self):
        r = Rating(id="my-rating")
        assert r.id == "my-rating"
        assert r.render()["id"] == "my-rating"
```

### Running Tests

```bash
uv run pytest tests/unit/test_rating.py -v
uv run pytest tests/ --cov=src/refast --cov-report=html
```

---

## Best Practices

1. **Always `snake_case` in `render()`** — never use `camelCase` prop keys in the Python
   `render()` method. The frontend converts them automatically.

2. **Type hints everywhere** — use `Literal`, `str | None`, `Any`, etc.

3. **Clamp/validate values** in `__init__` — don't leave invalid state to the frontend.

4. **Docstrings with examples** — document every prop, include a short usage snippet.

5. **Check callbacks for `None`** — always use `cb.serialize() if cb else None`.

6. **Use `**self._serialize_extra_props()`** — lets users pass arbitrary HTML attributes
   like `data_testid`, `aria_label`, etc.

7. **Tailwind CSS in React** — use `cn()` for class composition; never use inline styles.

8. **Include `data-refast-id`** — always accept and forward it to the root element so
   the framework can track component identity.

---

## Summary

| Step | What to do |
|------|-----------|
| 1 | Subclass `Component`, set `component_type`, implement `render()` with `snake_case` props |
| 2 | Export from `shadcn/__init__.py` and `components/__init__.py` |
| 3 | Create React functional component with `camelCase` props |
| 4 | Register React component in `registry.ts` |
| 5 | Write unit tests in `tests/unit/` |

## Next Steps

- [Building Extensions](/docs/advanced/extension-dev) — Package components as installable extensions
- [Styling](/docs/advanced/styling) — Tailwind CSS patterns and theming
- [Naming Conventions](/docs/advanced/styling) — Full `snake_case` ↔ `camelCase` reference
"""
