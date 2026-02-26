"""Callbacks & Events — /docs/concepts/callbacks."""

import asyncio

from refast.components import Button, Container, Heading, Input, Separator, Text
from refast.context import Context

from ..utils import render_markdown_with_demo_apps

PAGE_TITLE = "Callbacks & Events"
PAGE_ROUTE = "/docs/concepts/callbacks"

CONTENT = r"""
## Overview

Callbacks bridge browser events and Python over WebSocket. Each event sends the callback
ID, bound kwargs, optional prop values, and raw event data to the server before invoking
your function.

Different components support different event types (e.g. `on_click`, `on_change`, `on_keydown`),
but the callback pattern is consistent: create a callback with `ctx.callback()`, then pass
it to your component's event prop. Inside the callback, use `ctx` methods to update the UI,
show toasts, and more.

In addition to python callbacks (`ctx.callback`), you can run client-only JavaScript with
`ctx.js()` for instant interactivity without a server roundtrip, or combine both in one
event by calling chaining `ctx.js()` and `ctx.callback()` together using `ctx.chain()`,
or by invoking Python from JavaScript with `refast.invoke()`. You can also just store event
data in the browser without a server hop using `ctx.save_prop()`. We'll cover all these patterns
in this section.

## Basic usage

```python
async def handle_click(ctx: Context, item_id: str):
    await ctx.show_toast(f"Clicked {item_id}!", variant="success")

Button("Click Me", on_click=ctx.callback(handle_click, item_id="Item 1"))
```

{{ basic_demo }}

## Callback with bound args

Attach static kwargs when you create the callback. Great for passing IDs, variants, or
mode flags without relying on client props.

```python
async def send_order(ctx: Context, flavor: str):
    await ctx.show_toast(f"Queued {flavor}")

Button("Vanilla", on_click=ctx.callback(send_order, flavor="vanilla")),
Button("Mocha", on_click=ctx.callback(send_order, flavor="mocha"), variant="secondary"),
Button("Chai", on_click=ctx.callback(send_order, flavor="chai"), variant="outline"),
```

## save_prop + props

`ctx.save_prop(name)` captures event data in the browser without a server hop. Use
`props=[...]` when creating a callback to forward those client-side values to Python.

```python
Input(placeholder="Your name", on_change=ctx.save_prop("demo_prop_name"))
Button("Submit with props", on_click=ctx.callback(submit, props=["demo_prop_name"]))

async def submit(ctx: Context, demo_prop_name: str = ""):
    await ctx.show_toast(f"Hello, {demo_prop_name}!")
```

{{ prop_store_demo }}

## Client-only `ctx.js` (Press Enter)

Run JavaScript directly in the browser for responsive UX without a server roundtrip.

```python
Input(
    placeholder="Type and press Enter",
    on_keydown=ctx.js(
        '''
        if (event.key === 'Enter') {
            const label = document.getElementById('js-enter-status');
            if (label) label.textContent = `Enter pressed: ${event.value || ''}`;
        }
        '''
    ),
)
```

{{ js_enter_demo }}

## `ctx.js` calling Python (refast.invoke)

Use JavaScript to filter events client-side, then call a Python callback only when needed.

```python
async def on_enter(ctx: Context, value: str = ""):
    await ctx.update_text("js-invoke-status", f"Python received: {value}")

Input(
    on_keydown=ctx.js(
        '''
        if (event.key === 'Enter') {
            refast.invoke(args.on_submit, { value: event.value });
        }
        ''',
        on_submit=ctx.callback(on_enter),
    ),
)
```

{{ js_invoke_demo }}

## Chaining actions (serial vs parallel)

Fire multiple actions from one event. Default mode is serial; set `mode="parallel"` to
run them simultaneously.

```python
# Serial (default)
Button(
    "Serial chain",
    on_click=ctx.chain([
        ctx.callback(clear_chain_log),
        ctx.callback(chain_record, message="Serial step 1", delay=0.15),
        ctx.callback(chain_record, message="Serial step 2", delay=0.15),
    ]),
)


# Parallel
Button(
    "Parallel chain",
    on_click=ctx.chain([
        ctx.callback(clear_chain_log),
        ctx.chain([
            ctx.callback(chain_record, message="Parallel A (fast)", delay=0.05),
            ctx.callback(chain_record, message="Parallel B (slower)", delay=0.25),
        ], mode="parallel"),
    ], mode="serial"),
)
```


{{ chain_demo }}


## Next steps

- [State Management](/docs/concepts/state) — Persist data across callbacks
- [DOM Updates](/docs/concepts/updates) — Targeted replacements, appends, and prop updates
- [JavaScript Interop](/docs/concepts/js-interop) — Run browser code and call component methods
"""


def render(ctx):
    """Render the callbacks concept page with inline live demos."""
    from docs_site.app import docs_layout

    basic_demo = Container(
        id="callbacks-basic-demo",
        class_name="space-y-3",
        children=[
            Heading("Live demo: basic callback", level=3, class_name="text-lg font-semibold"),
            Text(
                "Clicking the button sends a callback with a bound argument to Python.",
                class_name="text-sm text-muted-foreground block",
            ),
            Button("Click Me", on_click=ctx.callback(handle_click, item_id="Item 1")),
        ],
    )

    bound_args_demo = Container(
        id="callbacks-bound-args",
        class_name="space-y-3",
        children=[
            Heading(
                "Live demo: ctx.callback bound args", level=3, class_name="text-lg font-semibold"
            ),
            Text(
                "Each button sends its flavor as a bound argument without reading client props.",
                class_name="text-sm text-muted-foreground block",
            ),
            Container(
                class_name="flex flex-wrap gap-2",
                children=[
                    Button("Vanilla", on_click=ctx.callback(demo_bound_arg, flavor="vanilla")),
                    Button(
                        "Mocha",
                        on_click=ctx.callback(demo_bound_arg, flavor="mocha"),
                        variant="secondary",
                    ),
                    Button(
                        "Chai",
                        on_click=ctx.callback(demo_bound_arg, flavor="chai"),
                        variant="outline",
                    ),
                ],
            ),
        ],
    )

    prop_store_demo = Container(
        id="callbacks-props-demo",
        class_name="space-y-4",
        children=[
            Heading("Live demo: save_prop + props", level=3, class_name="text-lg font-semibold"),
            Text(
                "Typing stores the value client-side via save_prop; the button forwards it to Python with props=[...].",
                class_name="text-sm text-muted-foreground",
            ),
            Input(
                id="callbacks-name-input",
                placeholder="Your name",
                on_change=ctx.save_prop("demo_prop_name"),
            ),
            Container(
                class_name="flex flex-wrap gap-2",
                children=[
                    Button(
                        "Submit with props",
                        on_click=ctx.callback(demo_prop_submit, props=["demo_prop_name"]),
                        variant="default",
                    ),
                    Button(
                        "Clear message",
                        on_click=ctx.callback(clear_prop_message),
                        variant="secondary",
                    ),
                ],
            ),
            Text(
                "Waiting for submission...",
                id="callbacks-props-status",
                class_name="text-sm text-muted-foreground",
            ),
        ],
    )

    js_enter_demo = Container(
        id="callbacks-js-enter",
        class_name="space-y-3",
        children=[
            Heading("Live demo: ctx.js (press Enter)", level=3, class_name="text-lg font-semibold"),
            Text(
                "Client-only JavaScript handles the Enter key and updates the status without a server call.",
                class_name="text-sm text-muted-foreground",
            ),
            Input(
                id="js-enter-input",
                placeholder="Type here and press Enter",
                on_keydown=ctx.js(
                    """
                    const label = document.getElementById('js-enter-status');
                    if (!label) return;
                    if (event.key === 'Enter') {
                        label.textContent = `Enter pressed: ${event.value || ''}`;
                        label.classList.remove('text-muted-foreground');
                        label.classList.add('text-emerald-600');
                    } else {
                        label.textContent = 'Waiting for Enter...';
                        label.classList.add('text-muted-foreground');
                        label.classList.remove('text-emerald-600');
                    }
                    """
                ),
            ),
            Text(
                "Waiting for Enter...",
                id="js-enter-status",
                class_name="text-sm text-muted-foreground",
            ),
        ],
    )

    js_invoke_demo = Container(
        id="callbacks-js-invoke",
        class_name="space-y-3",
        children=[
            Heading(
                "Live demo: ctx.js + refast.invoke", level=3, class_name="text-lg font-semibold"
            ),
            Text(
                "JavaScript filters events and only calls Python on Enter using refast.invoke().",
                class_name="text-sm text-muted-foreground",
            ),
            Input(
                id="js-invoke-input",
                placeholder="Type and press Enter to call Python",
                on_keydown=ctx.js(
                    """
                    if (event.key === 'Enter') {
                        refast.invoke(args.on_submit, { value: event.value });
                    }
                    """,
                    on_submit=ctx.callback(demo_invoke_python),
                ),
            ),
            Text(
                "Python has not run yet — press Enter to send a message.",
                id="js-invoke-status",
                class_name="text-sm text-muted-foreground",
            ),
        ],
    )

    chain_demo = Container(
        id="callbacks-chain",
        class_name="space-y-4",
        children=[
            Heading("Live demo: ctx.chain", level=3, class_name="text-lg font-semibold"),
            Text(
                "Serial runs actions one-by-one; parallel fires them together.",
                class_name="text-sm text-muted-foreground",
            ),
            Container(
                class_name="flex flex-wrap gap-2",
                children=[
                    Button(
                        "Serial chain",
                        on_click=ctx.chain(
                            [
                                ctx.callback(clear_chain_log),
                                ctx.callback(chain_record, message="Serial step 1", delay=0.15),
                                ctx.callback(chain_record, message="Serial step 2", delay=0.15),
                            ]
                        ),
                    ),
                    Button(
                        "Parallel chain",
                        on_click=ctx.chain(
                            [
                                ctx.callback(clear_chain_log),
                                ctx.chain(
                                    [
                                        ctx.callback(
                                            chain_record, message="Parallel A (fast)", delay=0.05
                                        ),
                                        ctx.callback(
                                            chain_record, message="Parallel B (slower)", delay=0.25
                                        ),
                                    ],
                                    mode="parallel",
                                ),
                            ]
                        ),
                        variant="secondary",
                    ),
                ],
            ),
            Container(
                id="chain-log",
                class_name="min-h-12 space-y-1 rounded-md border bg-white/60 p-3",
                children=[
                    Text(
                        "Run a chain to see events here.",
                        class_name="text-sm text-muted-foreground",
                    ),
                ],
            ),
        ],
    )

    content = Container(
        class_name="max-w-4xl mx-auto p-6 space-y-8",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            render_markdown_with_demo_apps(CONTENT, locals()),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


async def handle_click(ctx: Context, item_id: str) -> None:
    """Example callback handler for basic demo."""
    await ctx.show_toast(f"Clicked {item_id}!", variant="success")


async def demo_bound_arg(ctx: Context, flavor: str) -> None:
    """Show a toast using a bound argument passed at callback creation time."""
    await ctx.show_toast(f"Queued {flavor}", variant="success")


async def demo_prop_submit(ctx: Context, demo_prop_name: str = "") -> None:
    """Read a saved prop from the client and surface it in the UI."""
    who = (demo_prop_name or "friend").strip() or "friend"
    await ctx.update_text("callbacks-props-status", f"Server received: {who}")
    await ctx.show_toast(f"Hello, {who}!", variant="info")


async def clear_prop_message(ctx: Context) -> None:
    """Reset the prop demo status label."""
    await ctx.update_text("callbacks-props-status", "Waiting for submission...")
    await ctx.update_props("callbacks-name-input", {"value": ""})  # Clear the input field as well


async def demo_invoke_python(ctx: Context, value: str = "") -> None:
    """Handle JS-triggered submit via refast.invoke()."""
    cleaned = value.strip()
    label = cleaned or "(empty)"
    await ctx.update_text("js-invoke-status", f"Python received: {label}")
    await ctx.show_toast(f"Processed: {label}", variant="success")


async def clear_chain_log(ctx: Context) -> None:
    """Reset the chain log container."""
    await ctx.replace(
        "chain-log",
        Container(
            id="chain-log",
            class_name="min-h-12 space-y-1 rounded-md border bg-white/60 p-3",
            children=[],
        ),
    )


async def chain_record(ctx: Context, message: str, delay: float = 0.0) -> None:
    """Append a log entry to illustrate chain ordering."""
    if delay:
        await asyncio.sleep(delay)
    await ctx.append("chain-log", Text(message, class_name="text-sm font-mono"))
    await ctx.show_toast(message, variant="secondary")
