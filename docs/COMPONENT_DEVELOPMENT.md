# Refast Component Development Guide

This comprehensive guide explains how to create and register new components and component collections for the Refast framework. Components in Refast are Python classes that render to dictionaries, which the React frontend interprets and renders.

## Table of Contents

1. [Overview](#overview)
2. [Component Architecture](#component-architecture)
3. [Creating a Simple Component](#creating-a-simple-component)
4. [Creating a Component Collection](#creating-a-component-collection)
5. [Handling Events and Callbacks](#handling-events-and-callbacks)
   - [JavaScript Callbacks with `ctx.js()`](#javascript-callbacks-with-ctxjs)
   - [Executing JavaScript from Python Callbacks with `ctx.call_js()`](#executing-javascript-from-python-callbacks-with-ctxcall_js)
   - [Calling Bound Component Methods](#calling-bound-component-methods-with-ctxbound_js-and-ctxcall_bound_js)
6. [Creating the Frontend React Component](#creating-the-frontend-react-component)
   - [Exposing Component Methods](#exposing-component-methods)
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

### Prop Naming Convention: snake_case

**Important:** All prop names emitted from Python components' `render()` methods must use `snake_case`. The frontend `ComponentRenderer` automatically converts these to `camelCase` for React components.

```python
# ✅ CORRECT - Use snake_case in render()
def render(self) -> dict[str, Any]:
    return {
        "type": self.component_type,
        "id": self.id,
        "props": {
            "class_name": self.class_name,  # NOT className
            "on_click": self.on_click.serialize() if self.on_click else None,  # NOT onClick
            "read_only": self.read_only,  # NOT readOnly
        },
        "children": self._render_children(),
    }

# ❌ WRONG - Don't use camelCase in Python render() methods
def render(self) -> dict[str, Any]:
    return {
        "props": {
            "className": self.class_name,  # WRONG
            "onClick": self.on_click.serialize(),  # WRONG
        }
    }
```

This also applies to `ctx.update_props()` calls:
```python
# ✅ CORRECT
await ctx.update_props("my-component", {"foreground_color": "red", "is_disabled": True})

# ❌ WRONG  
await ctx.update_props("my-component", {"foregroundColor": "red", "isDisabled": True})
```

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
                "on_change": self.on_change.serialize() if self.on_change else None,
                "class_name": self.class_name,
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
                "class_name": self.class_name,
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
                "class_name": self.class_name,
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
            "on_click": self.on_click.serialize() if self.on_click else None,
            "on_change": self.on_change.serialize() if self.on_change else None,
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

### JavaScript Callbacks with `ctx.js()`

For interactions that don't require server-side processing, you can use `ctx.js()` to execute JavaScript directly in the browser. This provides immediate feedback without a WebSocket roundtrip.

#### When to Use `ctx.js()` vs `ctx.callback()`

| Use `ctx.js()` for | Use `ctx.callback()` for |
|-------------------|-------------------------|
| UI animations and transitions | Database operations |
| Toggling CSS classes | Server-side validation |
| Calling client-side libraries | State that needs persistence |
| Immediate visual feedback | Business logic |
| DOM manipulations (scroll, focus) | Multi-client broadcasts |

#### Basic Usage

```python
from refast import Context, RefastApp
from refast.components import Button, Input, Container

ui = RefastApp()

@ui.page("/")
def home(ctx: Context):
    return Container(
        children=[
            # Simple alert
            Button(
                "Show Alert",
                on_click=ctx.js("alert('Hello from JavaScript!')")
            ),
            
            # Toggle dark mode
            Button(
                "Toggle Theme",
                on_click=ctx.js("document.body.classList.toggle('dark')")
            ),
            
            # Log input value
            Input(
                placeholder="Type something...",
                on_change=ctx.js("console.log('Input value:', event.value)")
            ),
        ]
    )
```

#### Available Variables in JavaScript Callbacks

Inside the JavaScript code passed to `ctx.js()`, you have access to:

- **`event`**: The event data object with properties like `value`, `checked`, `name`
- **`args`**: The bound arguments passed to `ctx.js()`
- **`element`**: The DOM element that triggered the event (if applicable)

```python
# Access event data
Input(on_change=ctx.js("console.log('Value:', event.value)"))

# Access bound arguments
Button(
    "Delete Item",
    on_click=ctx.js(
        "confirm('Delete ' + args.name + '?') && window.pendingDelete(args.id)",
        id=item["id"],
        name=item["name"]
    )
)

# Access the triggering element
Button(
    "Animate",
    on_click=ctx.js("element.classList.add('animate-pulse')")
)
```

#### Calling External JavaScript Libraries

```python
# Confetti animation (requires confetti library)
Button(
    "Celebrate!",
    on_click=ctx.js("confetti({ particleCount: 100, spread: 70 })")
)

# Clipboard API
Button(
    "Copy to Clipboard",
    on_click=ctx.js(
        "navigator.clipboard.writeText(args.text).then(() => alert('Copied!'))",
        text="Hello, World!"
    )
)

# Local storage
Button(
    "Save Preference",
    on_click=ctx.js(
        "localStorage.setItem('theme', args.theme); location.reload()",
        theme="dark"
    )
)
```

#### Combining with Python Callbacks

You can use JavaScript for immediate feedback and Python for server operations:

```python
async def save_to_database(ctx: Context):
    """Save data to database after validation."""
    # This runs on the server
    data = ctx.event_data
    await database.save(data)
    await ctx.show_toast("Saved!", variant="success")

@ui.page("/")
def home(ctx: Context):
    return Button(
        "Save",
        # JS for immediate visual feedback
        on_click=ctx.js("this.disabled = true; this.textContent = 'Saving...'")
    )
    # For both, you'd typically use a separate loading state via ctx.callback()
```

### Executing JavaScript from Python Callbacks with `ctx.call_js()`

When you need to execute JavaScript from within a Python callback (after some server-side processing), use `ctx.call_js()`:

```python
async def save_and_celebrate(ctx: Context):
    """Save data and trigger client-side celebration."""
    # Server-side logic
    await database.save(ctx.event_data)
    ctx.state.set("saved", True)
    await ctx.push_update()
    
    # Trigger client-side JavaScript
    await ctx.call_js("confetti({ particleCount: 100 })")
    
    # Scroll to top
    await ctx.call_js("window.scrollTo({ top: 0, behavior: 'smooth' })")
    
    # Focus an input
    await ctx.call_js(
        "document.getElementById(args.input_id)?.focus()",
        input_id="next-field"
    )

@ui.page("/")
def form(ctx: Context):
    return Button(
        "Save & Celebrate",
        on_click=ctx.callback(save_and_celebrate)
    )
```

#### `ctx.call_js()` Use Cases

- Triggering animations after server operations complete
- Scrolling to specific elements after data loads
- Focusing inputs after form submissions
- Interacting with third-party JavaScript libraries
- Playing sounds or showing visual effects

#### Security Considerations

⚠️ **Important**: Never use user-provided strings directly in the `code` parameter:

```python
# ❌ DANGEROUS - Never do this!
user_input = request.query_params.get("action")
Button(on_click=ctx.js(user_input))  # XSS vulnerability!

# ✅ SAFE - Use bound arguments for user data
Button(
    on_click=ctx.js(
        "handleAction(args.action)",
        action=user_input  # Properly serialized, not executed as code
    )
)
```

Bound arguments are serialized as JSON data, not as executable code, making them safe to use with user-provided values.

### Calling Bound Component Methods with `ctx.bound_js()` and `ctx.call_bound_js()`

Some components expose imperative methods that can be called from Python. For example, a canvas component might expose `clearCanvas()`, `undo()`, or `loadPaths()` methods. Refast provides two ways to call these methods:

#### `ctx.bound_js()` - For Event Handlers (No Server Roundtrip)

Use `ctx.bound_js()` to call component methods directly from event handlers without a server roundtrip. This is similar to `ctx.js()` but specifically for calling methods on components:

```python
from refast import RefastApp, Context
from refast_sketch_canvas import SketchCanvas  # Example extension component

ui = RefastApp()

@ui.page("/")
def canvas_page(ctx: Context):
    return Container(
        children=[
            # Canvas component with an ID
            SketchCanvas(id="my-canvas", width="600px", height="400px"),
            
            # Control buttons that call canvas methods directly
            HStack(
                children=[
                    Button("Clear", on_click=ctx.bound_js("my-canvas", "clearCanvas")),
                    Button("Undo", on_click=ctx.bound_js("my-canvas", "undo")),
                    Button("Redo", on_click=ctx.bound_js("my-canvas", "redo")),
                    
                    # Method with arguments
                    Button(
                        "Eraser On",
                        on_click=ctx.bound_js("my-canvas", "eraseMode", erase=True)
                    ),
                    Button(
                        "Eraser Off",
                        on_click=ctx.bound_js("my-canvas", "eraseMode", erase=False)
                    ),
                ]
            ),
        ]
    )
```

#### `ctx.call_bound_js()` - For Server-Side Callbacks (With Server Roundtrip)

Use `ctx.call_bound_js()` when you need to call component methods from within a Python callback, typically after some server-side processing:

```python
async def load_saved_drawing(ctx: Context):
    """Load a saved drawing from the database."""
    drawing_id = ctx.event_data.get("drawing_id")
    
    # Fetch paths from database
    paths = await database.get_drawing(drawing_id)
    
    # Load the paths into the canvas
    await ctx.call_bound_js("my-canvas", "loadPaths", paths=paths)
    
    await ctx.show_toast("Drawing loaded!", variant="success")


async def clear_and_save_state(ctx: Context):
    """Clear canvas and update server state."""
    # Clear the canvas
    await ctx.call_bound_js("my-canvas", "clearCanvas")
    
    # Update server state
    ctx.state.set("canvas_cleared", True)
    await ctx.push_update()


@ui.page("/")
def canvas_page(ctx: Context):
    return Container(
        children=[
            SketchCanvas(id="my-canvas"),
            Button("Load Saved", on_click=ctx.callback(load_saved_drawing)),
            Button("Clear & Save", on_click=ctx.callback(clear_and_save_state)),
        ]
    )
```

#### When to Use Each Method

| Method | Use Case | Server Roundtrip |
|--------|----------|------------------|
| `ctx.bound_js()` | Simple UI interactions (clear, undo, toggle) | No |
| `ctx.call_bound_js()` | After server processing (load data, save state) | Yes |

#### Creating Components with Bound Methods

For components to support `ctx.bound_js()` and `ctx.call_bound_js()`, they must expose methods on their wrapper DOM element. See [Exposing Component Methods](#exposing-component-methods) in the Frontend React Component section below.

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

### Exposing Component Methods

To allow Python code to call methods on your component using `ctx.bound_js()` or `ctx.call_bound_js()`, you need to expose those methods on the wrapper DOM element. This pattern is essential for components with imperative APIs (like canvas, video players, or rich text editors).

#### Basic Pattern

Use `useRef`, `useEffect`, and optionally `useImperativeHandle` to expose methods:

```tsx
import React, { forwardRef, useRef, useEffect, useImperativeHandle } from 'react';

// Define the methods your component exposes
export interface MyComponentRef {
  clear: () => void;
  reset: () => void;
  getValue: () => string;
  setValue: (value: string) => void;
}

interface MyComponentProps {
  id?: string;
  className?: string;
  initialValue?: string;
  'data-refast-id'?: string;
}

export const MyComponent = forwardRef<MyComponentRef | null, MyComponentProps>(
  ({ id, className, initialValue = '', 'data-refast-id': dataRefastId }, ref) => {
    // Reference to the inner component or state
    const internalRef = useRef<HTMLInputElement>(null);
    // Reference to the wrapper div that will have methods attached
    const wrapperRef = useRef<HTMLDivElement>(null);
    const [value, setValue] = React.useState(initialValue);

    // Define the imperative methods
    const clear = () => setValue('');
    const reset = () => setValue(initialValue);
    const getValue = () => value;
    const setValueMethod = (newValue: string) => setValue(newValue);

    // Expose methods via useImperativeHandle (for React refs)
    useImperativeHandle(ref, () => ({
      clear,
      reset,
      getValue,
      setValue: setValueMethod,
    }));

    // CRITICAL: Attach methods to the wrapper DOM element
    // This allows ctx.bound_js() and ctx.call_bound_js() to find and call them
    useEffect(() => {
      const wrapper = wrapperRef.current;
      if (wrapper) {
        // Attach each method to the DOM element
        (wrapper as any).clear = clear;
        (wrapper as any).reset = reset;
        (wrapper as any).getValue = getValue;
        (wrapper as any).setValue = setValueMethod;
      }
      
      // Cleanup: remove methods when component unmounts
      return () => {
        if (wrapper) {
          delete (wrapper as any).clear;
          delete (wrapper as any).reset;
          delete (wrapper as any).getValue;
          delete (wrapper as any).setValue;
        }
      };
    }, [value, initialValue]); // Re-attach if dependencies change

    return (
      <div
        ref={wrapperRef}
        id={id}  // IMPORTANT: The id is used by ctx.bound_js() to find this element
        className={className}
        data-refast-id={dataRefastId}
      >
        <input
          ref={internalRef}
          value={value}
          onChange={(e) => setValue(e.target.value)}
        />
      </div>
    );
  }
);

MyComponent.displayName = 'MyComponent';
```

#### Complete Example: SketchCanvas Component

Here's a real-world example from the `refast-sketch-canvas` extension:

```tsx
import React, { forwardRef, useImperativeHandle, useRef } from 'react';
import { ReactSketchCanvas, type ReactSketchCanvasRef } from 'react-sketch-canvas';

export interface SketchCanvasProps {
  id?: string;
  className?: string;
  strokeColor?: string;
  // ... other props
  'data-refast-id'?: string;
}

export const SketchCanvas = forwardRef<ReactSketchCanvasRef | null, SketchCanvasProps>(
  ({ id, className, strokeColor = 'black', 'data-refast-id': dataRefastId, ...props }, ref) => {
    const canvasRef = useRef<ReactSketchCanvasRef>(null);
    const wrapperRef = useRef<HTMLDivElement>(null);

    // Expose methods via useImperativeHandle (for React refs)
    useImperativeHandle(ref, () => ({
      clearCanvas: () => canvasRef.current?.clearCanvas(),
      undo: () => canvasRef.current?.undo(),
      redo: () => canvasRef.current?.redo(),
      resetCanvas: () => canvasRef.current?.resetCanvas(),
      eraseMode: (erase: boolean) => canvasRef.current?.eraseMode(erase),
      exportImage: (imageType: "jpeg" | "png") => canvasRef.current?.exportImage(imageType),
      exportPaths: () => canvasRef.current?.exportPaths(),
      loadPaths: (paths: any[]) => canvasRef.current?.loadPaths(paths),
    } as any));

    // Attach methods to the DOM element for ctx.bound_js() / ctx.call_bound_js()
    React.useEffect(() => {
      const wrapper = wrapperRef.current;
      if (wrapper && canvasRef.current) {
        (wrapper as any).clearCanvas = () => canvasRef.current?.clearCanvas();
        (wrapper as any).undo = () => canvasRef.current?.undo();
        (wrapper as any).redo = () => canvasRef.current?.redo();
        (wrapper as any).resetCanvas = () => canvasRef.current?.resetCanvas();
        (wrapper as any).eraseMode = (erase: boolean) => canvasRef.current?.eraseMode(erase);
        (wrapper as any).exportImage = (imageType: "jpeg" | "png") => 
          canvasRef.current?.exportImage(imageType);
        (wrapper as any).exportPaths = () => canvasRef.current?.exportPaths();
        (wrapper as any).loadPaths = (paths: any[]) => canvasRef.current?.loadPaths(paths);
      }
    }, []);

    return (
      <div 
        ref={wrapperRef}
        id={id}  // Required for ctx.bound_js() to find this element
        className={className}
        data-refast-id={dataRefastId}
      >
        <ReactSketchCanvas
          ref={canvasRef}
          strokeColor={strokeColor}
          {...props}
        />
      </div>
    );
  }
);

SketchCanvas.displayName = 'SketchCanvas';
```

#### Documenting Component Methods

Components should document their available methods in the Python component class docstring:

```python
class SketchCanvas(Component):
    """
    Canvas component for drawing and sketching.
    
    Example:
        ```python
        SketchCanvas(
            id="my-canvas",
            stroke_color="blue",
            stroke_width=4,
        )
        ```
    
    Bound Methods (for ctx.bound_js() / ctx.call_bound_js()):
        - clearCanvas(): Clear all drawings from the canvas
        - undo(): Undo the last stroke
        - redo(): Redo the last undone stroke
        - resetCanvas(): Reset the canvas to initial state
        - eraseMode(erase: bool): Toggle eraser mode
        - exportImage(imageType: str): Export as "jpeg" or "png"
        - exportPaths(): Export drawing paths as JSON
        - loadPaths(paths: list): Load paths into the canvas
    
    Args:
        id: Component ID (required for bound method calls)
        stroke_color: Color of the stroke
        stroke_width: Width of the stroke
        # ... other args
    """
```

#### Key Points

1. **Wrapper Element ID**: The `id` prop must be set on the wrapper element that has the methods attached. This is how `ctx.bound_js()` finds the element.

2. **Method Attachment**: Methods are attached to the DOM element in a `useEffect` hook. This ensures they're available after the component mounts.

3. **Cleanup**: Remove methods in the cleanup function to prevent memory leaks and stale references.

4. **Dependency Array**: Include any values that methods depend on in the `useEffect` dependency array to ensure methods use current values.

5. **TypeScript**: Use `(element as any)` to bypass TypeScript's type checking when attaching methods to DOM elements, since DOM elements don't natively have custom methods.

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
        
        assert rendered["props"]["on_change"] == {"callbackId": "cb-123"}
    
    def test_rating_without_callback(self):
        """Test Rating without callback renders None."""
        rating = Rating(value=3)
        rendered = rating.render()
        
        assert rendered["props"]["on_change"] is None
    
    def test_rating_class_name(self):
        """Test Rating accepts className."""
        rating = Rating(value=3, class_name="my-rating")
        rendered = rating.render()
        
        assert rendered["props"]["class_name"] == "my-rating"
    
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
            "on_change": self.on_change.serialize() if self.on_change else None,
            # Standard props
            "class_name": self.class_name,
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
                "on_change": self.on_change.serialize() if self.on_change else None,
                "class_name": self.class_name,
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
        assert rendered["props"]["on_change"] is None
    
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
        
        assert rendered["props"]["on_change"]["callbackId"] == "cb-test-123"
    
    def test_rating_class_name(self):
        """Test Rating accepts class_name."""
        rating = Rating(class_name="custom-class")
        rendered = rating.render()
        
        assert rendered["props"]["class_name"] == "custom-class"
    
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

---

## Creating External Extensions

For creating third-party extensions (like wrapping existing React libraries as Refast components), please refer to the [Extension Development Guide](EXTENSION_DEVELOPMENT.md).
]

[project.urls]
"Homepage" = "https://github.com/yourusername/my-refast-extension"

# Entry point for auto-discovery by Refast
[project.entry-points."refast.extensions"]
my_extension = "my_refast_extension:MyExtension"

[tool.hatch.build.targets.wheel]
packages = ["src/my_refast_extension"]

[tool.hatch.build.targets.sdist]
include = [
    "src/",
    "frontend/",
    "README.md",
    "pyproject.toml",
    "hatch_build.py",
]

[tool.hatch.build.hooks.custom]
# Custom build hook defined in hatch_build.py
# Runs npm install && npm run build before packaging
path = "hatch_build.py"
```

### Step 7: Create the Build Hook

The build hook automatically compiles frontend assets when the package is built:

```python
# hatch_build.py
"""Custom Hatch build hook to build frontend assets before packaging."""

import os
import subprocess
from pathlib import Path
from typing import Any

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):
    """Build hook that compiles the React frontend before packaging."""

    PLUGIN_NAME = "custom"

    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        """
        Build the frontend assets before the package is built.

        This hook runs `npm install` and `npm run build` in the frontend
        directory to compile the React components into a UMD bundle.
        """
        root = Path(self.root)
        frontend_dir = root / "frontend"
        static_dir = root / "src" / "my_refast_extension" / "static"

        # Skip if we're in an sdist (source already built) or static exists
        if not frontend_dir.exists():
            self.app.display_info("Frontend directory not found, skipping build")
            return

        # Check if npm is available
        npm_cmd = "npm.cmd" if os.name == "nt" else "npm"
        
        try:
            subprocess.run(
                [npm_cmd, "--version"],
                check=True,
                capture_output=True,
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            if static_dir.exists() and any(static_dir.iterdir()):
                self.app.display_info(
                    "npm not found but static files exist, skipping build"
                )
                return
            raise RuntimeError(
                "npm is required to build the frontend. "
                "Please install Node.js or pre-build the frontend."
            )

        self.app.display_info("Installing frontend dependencies...")
        subprocess.run(
            [npm_cmd, "install"],
            cwd=frontend_dir,
            check=True,
            shell=(os.name == "nt"),
        )

        self.app.display_info("Building frontend assets...")
        subprocess.run(
            [npm_cmd, "run", "build"],
            cwd=frontend_dir,
            check=True,
            shell=(os.name == "nt"),
        )

        # Verify build output exists
        if not static_dir.exists() or not any(static_dir.iterdir()):
            raise RuntimeError(
                f"Frontend build did not produce output in {static_dir}"
            )

        self.app.display_info("Frontend build complete!")
```

### Building and Installing

With the hatch build hook, the frontend is built automatically:

```bash
# Install package locally (builds frontend automatically)
pip install -e .

# Or build a wheel/sdist distribution
pip install build
python -m build
```

For development, you can also build the frontend manually:

```bash
# Build frontend manually
cd frontend
npm install
npm run build  # Outputs to src/my_refast_extension/static/
```

### Using the Extension

Once installed, the extension is auto-discovered:

```python
from fastapi import FastAPI
from refast import RefastApp, Context
from my_refast_extension import MyComponent

ui = RefastApp()  # Extension auto-discovered!

@ui.page("/")
def home(ctx: Context):
    return MyComponent(value="Hello, World!")

app = FastAPI()
app.include_router(ui.router)
```

To disable auto-discovery and register manually:

```python
from my_refast_extension import MyExtension

ui = RefastApp(
    auto_discover_extensions=False,
    extensions=[MyExtension()],
)
```

### Extension Best Practices

1. **Use RefastClient's React**: Never bundle React in your extension. Always use `external: ['react', 'react-dom']` and reference `window.RefastClient.React`.

2. **Unique Names**: Use a unique `name` for your extension (e.g., `my-company-charts`) to avoid conflicts.

3. **Snake Case Props**: Python components should emit `snake_case` props. The frontend auto-converts to camelCase.

4. **Guard Registration**: Check `componentRegistry.has()` before registering to avoid duplicate registration errors.

5. **Error Handling**: Log clear error messages if RefastClient is not available.

6. **Static Assets**: Place built assets in `static/` directory and configure the hatch build hook for automatic compilation.

7. **Documentation**: Include docstrings in Python components and document all props in your README.

8. **Hatch Build Hook**: Use a custom hatch build hook to automatically compile frontend assets during package installation.

### Cookiecutter Template

For the fastest way to create a new Refast extension, use the cookiecutter template:

```bash
# Install cookiecutter
pip install cookiecutter

# Generate a new extension
cookiecutter gh:idling-mind/refast-extension-template
```

The template includes:
- Full project structure with Python backend and React frontend
- Hatch build system with automatic frontend compilation
- Entry point for auto-discovery by Refast
- TypeScript + Vite configuration
- Example component with proper prop handling and bound methods
- Optional example app demonstrating usage

### Complete Example: refast-sketch-canvas

See the [refast-sketch-canvas](https://github.com/idling-mind/refast-sketch-canvas) package for a complete working example of a Refast extension.

