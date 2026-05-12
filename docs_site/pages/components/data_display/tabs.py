"""Tabs — /docs/components/tabs.

Interactive reference page for the Tabs component family.
"""

from refast import Context
from refast.components import (
    Card,
    CardContent,
    CardHeader,
    Checkbox,
    Column,
    Container,
    Heading,
    Markdown,
    Row,
    Select,
    Separator,
    TabItem,
    Tabs,
    Text,
)
from docs_site.pages.components.playground import playground_card

PAGE_TITLE = "Tabs"
PAGE_ROUTE = "/docs/components/tabs"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_tab_count(ctx: Context, value: str):
    ctx.state.set("tbs_count", value)
    await ctx.refresh()


async def _set_active_tab(ctx: Context, value: str):
    ctx.state.set("tbs_active", value)
    await ctx.refresh()


async def _set_controlled(ctx: Context, value: bool):
    ctx.state.set("tbs_controlled", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────

_TAB_LABELS = ["Account", "Password", "Notifications", "Billing"]
_TAB_CONTENT = [
    "Manage your account settings and profile information.",
    "Change your password and configure two-factor authentication.",
    "Configure how and when you receive notifications.",
    "Manage your subscription plan and payment methods.",
]


def _playground(ctx: Context):
    tab_count = int(ctx.state.get("tbs_count", "3"))
    controlled = ctx.state.get("tbs_controlled", False)
    active_tab = ctx.state.get("tbs_active", "tab-0")

    tab_items = [
        TabItem(
            value=f"tab-{i}",
            label=_TAB_LABELS[i],
            children=[
                Container(
                    class_name="pt-4",
                    children=[
                        Text(_TAB_CONTENT[i], class_name="text-sm text-muted-foreground"),
                    ],
                )
            ],
        )
        for i in range(tab_count)
    ]

    if controlled:
        tabs = Tabs(
            value=active_tab,
            on_value_change=ctx.callback(_set_active_tab),
            children=tab_items,
        )
    else:
        tabs = Tabs(
            default_value="tab-0",
            children=tab_items,
        )

    return playground_card(
        options=[
            Column(
                gap=1,
                children=[
                    Text("Tab count", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": "2", "label": "2 tabs"},
                            {"value": "3", "label": "3 tabs"},
                            {"value": "4", "label": "4 tabs"},
                        ],
                        value=str(tab_count),
                        on_change=ctx.callback(_set_tab_count),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("Mode", class_name="text-sm font-medium"),
                    Checkbox(
                        label="controlled (Python manages active tab)",
                        checked=controlled,
                        on_change=ctx.callback(_set_controlled),
                    ),
                ],
            ),
        ],
        preview=[tabs],
        code=Markdown(
            content=(
                "```python\n"
                + (
                    f"# Controlled — Python tracks active tab\n"
                    f"Tabs(\n"
                    f'    value="{active_tab}",\n'
                    f"    on_value_change=ctx.callback(set_active_tab),\n"
                    f"    children=[\n"
                    if controlled
                    else (
                        "# Uncontrolled — browser manages state\n"
                        "Tabs(\n"
                        '    default_value="tab-0",\n'
                        "    children=[\n"
                    )
                )
                + "".join(
                    f'        TabItem(value="tab-{i}", label="{_TAB_LABELS[i]}", children=[...]),\n'
                    for i in range(tab_count)
                )
                + "    ],\n"
                ")\n"
                "```"
            )
        ),
        preview_class="border rounded-lg p-4 bg-muted/30",
    )


# ── Render ────────────────────────────────────────────────────────────────


def render(ctx: Context):
    """Render the Tabs component reference page."""
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
Tab panels for switching between related views. Each `TabItem` bundles
the trigger button and its content panel into a single component.

```python
from refast.components import Tabs, TabItem

Tabs(
    default_value="overview",
    children=[
        TabItem(
            value="overview",
            label="Overview",
            children=[Text("Overview content here.")],
        ),
        TabItem(
            value="settings",
            label="Settings",
            children=[Text("Settings content here.")],
        ),
    ],
)
```
"""

REFERENCE = """
## Tabs Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | `TabItem` components. |
| `default_value` | `str \\| None` | `None` | Initially active tab value (uncontrolled). |
| `value` | `str \\| None` | `None` | Controlled active tab value. |
| `on_value_change` | `Callback \\| None` | `None` | Fired when the active tab changes. `ctx.event_data` is the new value string. |
| `class_name` | `str` | `""` | Extra Tailwind classes. |

## TabItem Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | `str` | *(required)* | Unique identifier within the `Tabs` group. |
| `label` | `str` | *(required)* | Text displayed on the tab trigger button. |
| `icon` | `str \\| None` | `None` | Lucide icon name shown before the label. |
| `children` | `list` | `[]` | Panel content shown when this tab is active. |
| `disabled` | `bool` | `False` | Grays out and disables the tab trigger. |
| `class_name` | `str` | `""` | Extra Tailwind classes. |

## Uncontrolled (browser state)

```python
Tabs(
    default_value="tab1",
    children=[
        TabItem(value="tab1", label="Tab 1", children=[Text("Content 1")]),
        TabItem(value="tab2", label="Tab 2", children=[Text("Content 2")]),
    ],
)
```

## Controlled (Python state)

```python
async def set_tab(ctx: Context, value: str):
    ctx.state.set("active_tab", value)
    await ctx.refresh()

def render(ctx: Context):
    active = ctx.state.get("active_tab", "tab1")
    return Tabs(
        value=active,
        on_value_change=ctx.callback(set_tab),
        children=[
            TabItem(value="tab1", label="Tab 1", children=[Text("Content 1")]),
            TabItem(value="tab2", label="Tab 2", children=[Text("Content 2")]),
        ],
    )
```

## Tabs with icons

```python
Tabs(
    default_value="profile",
    children=[
        TabItem(value="profile", label="Profile", icon="user"),
        TabItem(value="settings", label="Settings", icon="settings"),
        TabItem(value="billing", label="Billing", icon="credit-card"),
    ],
)
```
"""
