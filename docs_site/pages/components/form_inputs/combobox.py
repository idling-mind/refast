"""Combobox — /docs/components/combobox."""
from refast import Context
from refast.components import (
    Alert,
    Badge,
    Card,
    CardContent,
    CardHeader,
    Checkbox,
    Column,
    Container,
    Heading,
    Markdown,
    Row,
    Separator,
    Text,
)
from refast.components.shadcn.controls import Combobox, ComboboxOption
from docs_site.pages.components.playground import playground_card

PAGE_TITLE = "Combobox"
PAGE_ROUTE = "/docs/components/combobox"

_FRAMEWORK_OPTIONS = [
    {"value": "next", "label": "Next.js", "description": "The React Framework"},
    {"value": "react", "label": "React", "description": "A UI library"},
    {"value": "vue", "label": "Vue", "description": "The Progressive Framework"},
    {"value": "svelte", "label": "Svelte", "description": "Cybernetically enhanced"},
    {"value": "astro", "label": "Astro", "description": "Build faster websites"},
    {"value": "nuxt", "label": "Nuxt", "description": "The Intuitive Vue Framework"},
    {"value": "remix", "label": "Remix", "description": "Full stack web framework"},
]

_FRAMEWORK_OPTIONS_ITEMS = [ComboboxOption(**opt) for opt in _FRAMEWORK_OPTIONS]


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_disabled(ctx: Context, value: bool):
    ctx.state.set("cmb_disabled", value)
    await ctx.refresh()


async def _set_required(ctx: Context, value: bool):
    ctx.state.set("cmb_required", value)
    await ctx.refresh()


async def _set_multiselect(ctx: Context, value: bool):
    ctx.state.set("cmb_multi", value)
    ctx.state.set("cmb_value", None)
    await ctx.refresh()


async def _set_error(ctx: Context, value: bool):
    ctx.state.set("cmb_error", value)
    await ctx.refresh()


async def _on_select(ctx: Context, value):
    ctx.state.set("cmb_value", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    disabled = ctx.state.get("cmb_disabled", False)
    required = ctx.state.get("cmb_required", False)
    multiselect = ctx.state.get("cmb_multi", False)
    show_error = ctx.state.get("cmb_error", False)
    selected = ctx.state.get("cmb_value", None)

    return playground_card(
        options=[
            Column(
                gap=1,
                children=[
                    Text("disabled", class_name="text-sm font-medium"),
                    Checkbox(
                        label="disabled",
                        checked=disabled,
                        on_change=ctx.callback(_set_disabled),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("required", class_name="text-sm font-medium"),
                    Checkbox(
                        label="required",
                        checked=required,
                        on_change=ctx.callback(_set_required),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("multiselect", class_name="text-sm font-medium"),
                    Checkbox(
                        label="multiselect",
                        checked=multiselect,
                        on_change=ctx.callback(_set_multiselect),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("error", class_name="text-sm font-medium"),
                    Checkbox(
                        label="show error",
                        checked=show_error,
                        on_change=ctx.callback(_set_error),
                    ),
                ],
            ),
        ],
        preview=[
            Combobox(
                label="Framework",
                description="Choose your primary framework.",
                options=_FRAMEWORK_OPTIONS_ITEMS,
                value=selected,
                placeholder="Select framework\u2026",
                search_placeholder="Search frameworks\u2026",
                empty_text="No frameworks found.",
                multiselect=multiselect,
                disabled=disabled,
                required=required,
                error="Please select an option." if show_error else None,
                on_select=ctx.callback(_on_select),
            )
        ],
        code=Markdown(
            content=(
                f"```python\n"
                f"Combobox(\n"
                f'    label="Framework",\n'
                f"    options=[\n"
                f'        {{"value": "next", "label": "Next.js", "description": "The React Framework"}},\n'
                f"        ...\n"
                f"    ],\n"
                f'    placeholder="Select framework\u2026",\n'
                f"    multiselect={multiselect},\n"
                f"    disabled={disabled},\n"
                f"    required={required},\n"
                f"    on_select=ctx.callback(handle_select),\n"
                f")\n"
                f"```"
            )
        ),
    )


# ── Render ────────────────────────────────────────────────────────────────


def render(ctx: Context):
    """Render the Combobox component reference page."""
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
A searchable dropdown with type-ahead filtering and optional multi-select.
Options are dicts with required `value` and `label` keys.

```python
from refast.components.shadcn.controls import Combobox

Combobox(
    label="Framework",
    options=[
        {"value": "next", "label": "Next.js"},
        {"value": "react", "label": "React"},
        {"value": "vue", "label": "Vue"},
    ],
    placeholder="Select framework\u2026",
    on_select=ctx.callback(handle_select),
)
```
"""

REFERENCE = """
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `options` | `list[dict]` | `[]` | Options with required `value` and `label` keys |
| `value` | `str \\| list[str] \\| None` | `None` | Controlled selected value(s) |
| `placeholder` | `str` | `"Select..."` | Trigger text when nothing is selected |
| `search_placeholder` | `str` | `"Search..."` | Placeholder in the search input |
| `empty_text` | `str` | `"No results found."` | Text when no options match |
| `multiselect` | `bool` | `False` | Allow selecting multiple values |
| `disabled` | `bool` | `False` | Disables interaction |
| `label` | `str \\| None` | `None` | Label text |
| `description` | `str \\| None` | `None` | Help text below label |
| `required` | `bool` | `False` | Shows required asterisk |
| `error` | `str \\| None` | `None` | Error message |
| `on_select` | `Callback \\| None` | `None` | Fired when selection changes |

## Rich Options

Options can include optional metadata for richer display:

```python
options=[
    {
        "value": "python",
        "label": "Python",
        "description": "A versatile language",
        "icon": "Code",
    },
]
```
"""
