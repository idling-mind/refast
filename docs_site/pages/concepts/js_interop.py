"""JavaScript Interop — /docs/concepts/js-interop."""

from refast.components import Button, Container, Heading, Input, Separator, Text
from refast.context import Context

from ..utils import render_markdown_with_demo_apps

PAGE_TITLE = "JavaScript Interop"
PAGE_ROUTE = "/docs/concepts/js-interop"


# ---------------------------------------------------------------------------
# Module-level callbacks (stable identity across re-renders)
# ---------------------------------------------------------------------------


async def handle_invoke(ctx: Context, value: str = "") -> None:
    """Receive a value sent from JavaScript via refast.invoke."""
    await ctx.update_text("js-invoke-result", f'Python received: "{value}"')


async def handle_call_js(ctx: Context) -> None:
    """Python callback that then pushes JS back to the browser."""
    import datetime

    now = datetime.datetime.now().strftime("%H:%M:%S")
    await ctx.call_js(
        "document.getElementById(args.targetId).textContent = args.msg",
        targetId="call-js-result",
        msg=f"Python ran at {now} — now JS updated this text!",
    )


# ---------------------------------------------------------------------------
# render
# ---------------------------------------------------------------------------


def render(ctx):
    """Render the JS interop concept page."""
    from docs_site.app import docs_layout

    # ------------------------------------------------------------------
    # Demo 1 — ctx.js() toggling a CSS class (pure client-side)
    # ------------------------------------------------------------------
    js_toggle_demo = Container(
        id="js-toggle-demo",
        class_name="space-y-3",
        children=[
            Heading("Live demo: ctx.js()", level=3, class_name="text-lg font-semibold"),
            Text(
                "Click the button — no server roundtrip, the browser handles it entirely.",
                class_name="text-sm text-muted-foreground block",
            ),
            Text(
                "This text can be highlighted by client-side JS.",
                id="js-toggle-text",
                class_name="p-2 rounded transition-colors duration-300",
            ),
            Container(
                class_name="flex gap-2",
                children=[
                    Button(
                        "Highlight",
                        on_click=ctx.js(
                            "document.getElementById('js-toggle-text').classList.add('bg-yellow-200','dark:bg-yellow-800')"
                        ),
                    ),
                    Button(
                        "Clear",
                        variant="outline",
                        on_click=ctx.js(
                            "document.getElementById('js-toggle-text').classList.remove('bg-yellow-200','dark:bg-yellow-800')"
                        ),
                    ),
                ],
            ),
        ],
    )

    # ------------------------------------------------------------------
    # Demo 2 — ctx.js() + refast.invoke() bridging back to Python
    # ------------------------------------------------------------------
    js_invoke_demo = Container(
        id="js-invoke-demo",
        class_name="space-y-3",
        children=[
            Heading(
                "Live demo: refast.invoke() bridge",
                level=3,
                class_name="text-lg font-semibold",
            ),
            Text(
                "Type something and press Enter — JS filters the key, then calls Python only on Enter.",
                class_name="text-sm text-muted-foreground block",
            ),
            Input(
                placeholder="Type and press Enter…",
                on_keydown=ctx.js(
                    """
                    if (event.key === 'Enter') {
                        refast.invoke(args.on_submit, { value: event.value });
                    }
                    """,
                    on_submit=ctx.callback(handle_invoke),
                ),
            ),
            Text(
                "Waiting for Enter…",
                id="js-invoke-result",
                class_name="text-sm text-muted-foreground",
            ),
        ],
    )

    # ------------------------------------------------------------------
    # Demo 3 — ctx.call_js() running JS from inside a Python callback
    # ------------------------------------------------------------------
    call_js_demo = Container(
        id="call-js-demo",
        class_name="space-y-3",
        children=[
            Heading(
                "Live demo: ctx.call_js()",
                level=3,
                class_name="text-lg font-semibold",
            ),
            Text(
                "Clicking runs a Python callback first, which then pushes JS back to the browser.",
                class_name="text-sm text-muted-foreground block",
            ),
            Button("Run Python → JS", on_click=ctx.callback(handle_call_js)),
            Text(
                "Result will appear here…",
                id="call-js-result",
                class_name="text-sm font-mono p-2 bg-muted rounded",
            ),
        ],
    )

    content = Container(
        class_name="max-w-4xl mx-auto p-6",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            render_markdown_with_demo_apps(CONTENT, locals()),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


CONTENT = r"""
## Overview

Sometimes you need client-side logic without a server roundtrip — animations, DOM
manipulation, localStorage access, or third-party JS library calls. Refast provides
four JavaScript interop methods on the `Context` object, split into two categories:

- **Event-handler callbacks** (`ctx.js()`, `ctx.bound_js()`) — returned as values and
  assigned to component event props. They run in the browser when the user interacts
  with the component, with no server roundtrip.
- **Imperative calls** (`ctx.call_js()`, `ctx.call_bound_js()`) — called with `await`
  inside an async Python callback. They send a WebSocket message that the browser
  executes immediately.

---

## ctx.js() — Client-Side Event Callback

Returns a `JsCallback` for use in event handler props (`on_click`, `on_change`, etc.).
No server roundtrip occurs; the code runs entirely in the browser.

```python
def js(
    self,
    code: str,
    *,
    debounce: int = 0,
    throttle: int = 0,
    **bound_args,
) -> JsCallback:
```

Inside `code` the following globals are available:

| Name | Description |
|------|-------------|
| `event` | Event data — `value`, `checked`, `key`, `name`, etc. |
| `args` | Any `bound_args` passed from Python |
| `element` | The DOM element that triggered the event |
| `refast` | Helper object — `refast.invoke(callback, data)` calls a Python callback |

**Basic example:**

```python
Button(
    "Highlight",
    on_click=ctx.js(
        "document.getElementById('my-text').classList.add('bg-yellow-200')"
    ),
)
```

{{ js_toggle_demo }}

**Reading event data:**

```python
Input(
    on_change=ctx.js("console.log('New value:', event.value)"),
)
```

**Debounce / throttle:**

```python
Input(
    on_change=ctx.js("console.log(event.value)", debounce=300),
)
```

**Bridging back to Python with `refast.invoke`:**

Pass a serialized Python callback as a bound arg and call it from JS:

```python
Input(
    on_keydown=ctx.js(
        '''
        if (event.key === 'Enter') {
            refast.invoke(args.on_submit, { value: event.value });
        }
        ''',
        on_submit=ctx.callback(handle_submit),
    )
)
```

{{ js_invoke_demo }}

---

## ctx.bound_js() — Call a Component Method as an Event Handler

Returns a `BoundJsCallback` that calls a named method on the DOM element of the
component identified by `target_id`. Useful for components that expose imperative
APIs (canvas drawing, video players, dialogs, etc.).

```python
def bound_js(
    self,
    target_id: str,
    method_name: str,
    *args,
    debounce: int = 0,
    throttle: int = 0,
    **kwargs,
) -> BoundJsCallback:
```

```python
Button("Play", on_click=ctx.bound_js("my-video", "play"))
Button("Show Dialog", on_click=ctx.bound_js("my-dialog", "showModal"))
Button("Eraser", on_click=ctx.bound_js("my-canvas", "setMode", "erase"))
```

Positional `args` and keyword `kwargs` are forwarded to the method call on the
element.

---

## ctx.call_js() — Imperatively Execute JS from Python

Awaitable. Sends a `js_exec` WebSocket message that the browser executes
immediately. Use this inside async Python callbacks when you need to trigger
browser-side behaviour after processing server-side logic.

```python
async def call_js(self, code: str, **args) -> None:
```

`args` are available inside `code` as the `args` object, exactly like `ctx.js()`.

```python
async def save_complete(ctx: Context):
    await db.save(ctx.event_data)
    await ctx.refresh()
    await ctx.call_js("confetti({ particleCount: 100 })")

async def focus_search(ctx: Context):
    await ctx.call_js(
        "document.getElementById(args.inputId)?.focus()",
        inputId="search-input",
    )
```

{{ call_js_demo }}

---

## ctx.call_bound_js() — Imperatively Call a Component Method from Python

Awaitable. Sends a `bound_method_call` WebSocket message that calls a named method
on a component's DOM element. Use inside async Python callbacks when the method call
depends on server-side data.

```python
async def call_bound_js(
    self,
    target_id: str,
    method_name: str,
    *args,
    **kwargs,
) -> None:
```

```python
async def load_drawing(ctx: Context):
    paths = await db.get_drawing(ctx.event_data["id"])
    await ctx.call_bound_js("my-canvas", "loadPaths", paths=paths)

async def draw_shape(ctx: Context):
    await ctx.call_bound_js("my-canvas", "drawShape", "circle", x=100, y=200)
```

---

## Summary

| Method | Type | Returns | Server Roundtrip? |
|--------|------|---------|-------------------|
| `ctx.js(code, **bound_args)` | Event-handler prop | `JsCallback` | No |
| `ctx.bound_js(id, method, *args)` | Event-handler prop | `BoundJsCallback` | No |
| `await ctx.call_js(code, **args)` | Imperative (in callback) | `None` | No — sent via WS |
| `await ctx.call_bound_js(id, method)` | Imperative (in callback) | `None` | No — sent via WS |
| `ctx.callback(fn)` | Event-handler prop | `Callback` | Yes |

---

## When to Use JS vs Python Callbacks

**Use JS callbacks (`ctx.js`, `ctx.bound_js`)** for:
- UI-only interactions (toggle class, scroll, focus)
- Performance-sensitive actions (hover effects, real-time input feedback)
- Browser API access (clipboard, geolocation, media)

**Use imperative JS (`ctx.call_js`, `ctx.call_bound_js`)** for:
- Triggering browser behaviour *after* server-side logic completes
- Animations or third-party library calls that depend on server data

**Use Python callbacks (`ctx.callback`)** for:
- Business logic, data processing
- State changes that affect the UI
- Database or API operations

---

## Next Steps

- [Building Components](/docs/advanced/component-dev) — Custom component development
- [Building Extensions](/docs/advanced/extension-dev) — Packaging reusable functionality
"""
