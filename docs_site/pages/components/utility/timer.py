"""Timer — /docs/components/timer."""

from docs_site.pages.components.playground import playground_card
from refast import Context
from refast.components import (
    Badge,
    Checkbox,
    Column,
    Container,
    Heading,
    Markdown,
    Row,
    Select,
    Separator,
    Text,
)
from refast.components.shadcn.timer import Timer

PAGE_TITLE = "Timer"
PAGE_ROUTE = "/docs/components/timer"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _on_tick(ctx: Context):
    count = ctx.state.get("timer_count", 0) + 1
    ctx.state.set("timer_count", count)
    await ctx.update_text("timer-tick-count", str(count))


async def _toggle_enabled(ctx: Context):
    enabled = ctx.state.get("timer_enabled", True)
    ctx.state.set("timer_enabled", not enabled)
    if not enabled:
        ctx.state.set("timer_count", 0)
    await ctx.refresh()


async def _set_interval(ctx: Context, value: str):
    ctx.state.set("timer_interval", int(value))
    ctx.state.set("timer_count", 0)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    enabled = ctx.state.get("timer_enabled", True)
    interval = ctx.state.get("timer_interval", 1000)
    count = ctx.state.get("timer_count", 0)

    return playground_card(
        options=[
            Row(
                gap=2,
                align="center",
                children=[
                    Checkbox(
                        label="Enabled",
                        checked=enabled,
                        on_change=ctx.callback(_toggle_enabled),
                    ),
                ],
            ),
            Select(
                label="Interval",
                value=str(interval),
                options=[
                    {"label": "500 ms", "value": "500"},
                    {"label": "1 s", "value": "1000"},
                    {"label": "2 s", "value": "2000"},
                    {"label": "5 s", "value": "5000"},
                ],
                on_change=ctx.callback(_set_interval),
            ),
        ],
        preview=[
            Column(
                gap=3,
                children=[
                    Row(
                        gap=3,
                        align="center",
                        children=[
                            Text(
                                "Status:",
                                class_name="text-sm font-medium",
                            ),
                            Badge(
                                children="Running" if enabled else "Paused",
                                variant="default" if enabled else "secondary",
                            ),
                        ],
                    ),
                    Row(
                        gap=3,
                        align="center",
                        children=[
                            Text("Ticks:", class_name="text-sm font-medium"),
                            Text(
                                str(count),
                                id="timer-tick-count",
                                class_name="text-2xl font-mono font-bold tabular-nums text-primary",
                            ),
                        ],
                    ),
                    Text(
                        f"Firing every {interval} ms",
                        class_name="text-xs text-muted-foreground",
                    ),
                ],
            ),
            # The invisible timer component
            Timer(
                interval=interval,
                enabled=enabled,
                on_tick=ctx.callback(_on_tick),
            ),
        ],
        code=Markdown(
            content=(
                "```python\n"
                "from refast.components import Timer\n\n"
                "Timer(\n"
                f"    interval={interval},\n"
                f"    enabled={enabled},\n"
                "    on_tick=ctx.callback(handle_tick),\n"
                ")\n\n"
                "async def handle_tick(ctx):\n"
                "    # called every tick\n"
                "    await ctx.refresh()\n"
                "```"
            )
        ),
        preview_class="border rounded-lg p-4 bg-muted/30",
    )


# ── Render ────────────────────────────────────────────────────────────────


def render(ctx: Context):
    """Render the Timer component reference page."""
    from docs_site.app import docs_layout

    content = Container(
        class_name="max-w-4xl mx-auto p-6",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            Markdown(content=INTRO),
            _playground(ctx),
            Markdown(content=REFERENCE),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


# ── Content ───────────────────────────────────────────────────────────────

INTRO = """
An invisible component that repeatedly fires a server callback at a fixed
interval.  It renders nothing in the DOM — place it anywhere in the component
tree and it will keep ticking as long as `enabled=True`.

```python
from refast.components import Timer

Timer(
    interval=2000,        # fire every 2 seconds
    enabled=True,
    on_tick=ctx.callback(handle_tick),
)

async def handle_tick(ctx):
    data = await fetch_latest()
    ctx.state.set("data", data)
    await ctx.refresh()
```

Toggle the timer on and off by updating the `enabled` prop from a callback or
state change — no need to add/remove the component from the tree.
"""

REFERENCE = """
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `interval` | `int` | `1000` | Milliseconds between ticks. Must be ≥ 100 |
| `enabled` | `bool` | `True` | When `False` the timer is paused; no callbacks are fired |
| `on_tick` | `Callback \\| None` | `None` | Server callback invoked on each tick |
| `id` | `str \\| None` | `None` | Unique element ID |
| `extra_props` | `dict \\| None` | `None` | Additional props forwarded to the component |

## Common Patterns

### Live Dashboard

Poll a data source periodically and refresh the UI:

```python
async def refresh_stats(ctx):
    stats = await fetch_stats()
    ctx.state.set("stats", stats)
    await ctx.refresh()

# In the page render:
Timer(interval=5000, on_tick=ctx.callback(refresh_stats))
```

### Toggle On / Off

Bind `enabled` to a state value controlled by a button:

```python
async def toggle_timer(ctx):
    ctx.state.set("running", not ctx.state.get("running", False))
    await ctx.refresh()

running = ctx.state.get("running", False)

Timer(interval=1000, enabled=running, on_tick=ctx.callback(handle_tick))
Button("Start" if not running else "Stop", on_click=ctx.callback(toggle_timer))
```

### One-Shot Countdown

Disable the timer inside its own callback after a fixed number of ticks:

```python
async def countdown_tick(ctx):
    remaining = ctx.state.get("remaining", 10) - 1
    ctx.state.set("remaining", remaining)
    if remaining <= 0:
        ctx.state.set("timer_enabled", False)
    await ctx.refresh()
```
"""
