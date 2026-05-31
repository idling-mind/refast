# Refast — Components & Layout Reference

All components are importable from `refast.components`:

```python
from refast import components as rc          # namespace import
from refast.components import Button, Row, Column, Text  # named imports
```

Every component accepts these universal kwargs:
- `id: str | None` — used for targeting with `ctx.replace()`, `ctx.append()`, etc.
- `class_name: str` — Tailwind CSS utility classes
- `style: dict` — inline CSS dict with camelCase keys (React style)
- `children: list | Any` — child components or strings. `None` values in lists are silently filtered.
- `extra_props: dict` — pass arbitrary HTML/React props through

---

## Children Pattern

`children` accepts a single component, a string, or a list. `None` in lists is filtered — useful for conditionals:

```python
rc.Column(children=[
    rc.Alert(title="Error", variant="destructive") if errors else None,  # filtered if None
    rc.Input(name="email"),
    rc.Button("Submit"),
])
```

---

## 1. Base / Primitive Components

### `Container`
Generic `<div>` wrapper. Add Tailwind via `class_name`.
```python
rc.Container(
    id="main",
    class_name="p-4 bg-background max-w-4xl mx-auto",
    style={"maxWidth": "72rem"},
    children=[...],
)
```

### `Text`
Inline text span.
```python
rc.Text("Hello!", class_name="text-sm font-medium text-muted-foreground")
```

### `Fragment`
Groups children with no DOM wrapper.
```python
rc.Fragment([rc.Text("Line 1"), rc.Text("Line 2")])
```

---

## 2. Layout Components

### `Row`
Horizontal flex container.
```python
rc.Row(
    children=[rc.Button("A"), rc.Button("B")],
    justify="between",   # "start"|"end"|"center"|"between"|"around"|"evenly"
    align="center",      # "start"|"end"|"center"|"stretch"|"baseline"
    gap=4,               # Tailwind spacing integer (×0.25rem)
    wrap=False,
    class_name="w-full",
)
```

### `Column`
Vertical flex container. Same props as `Row`.
```python
rc.Column(
    children=[rc.Text("Line 1"), rc.Text("Line 2")],
    gap=2,
    align="stretch",
)
```

### `Grid`
CSS Grid container.
```python
rc.Grid(
    children=[rc.Card(...) for _ in range(6)],
    columns=3,           # int or CSS string like "1fr 2fr"
    rows=None,           # int or CSS string; None = auto
    gap=4,
)
```

### `Flex`
Full directional flexbox (row/column/reverse). Use `Row`/`Column` for most cases.
```python
rc.Flex(
    direction="row-reverse",   # "row"|"column"|"row-reverse"|"column-reverse"
    justify="between",
    align="center",
    wrap=True,
    gap=2,
    children=[...],
)
```

### `Center`
Centers children both horizontally and vertically.
```python
rc.Center(
    class_name="h-screen",
    children=[rc.Heading("Welcome", level=1)],
)
```

---

## 3. Typography Components

### `Heading`
```python
rc.Heading("Welcome", level=1)            # level: 1–6
rc.Heading("Section", level=2, class_name="text-blue-500")
```

### `Paragraph`
```python
rc.Paragraph("Regular text.")
rc.Paragraph("Lead paragraph.", lead=True)     # larger/emphasized
rc.Paragraph("Muted note.", muted=True)        # muted-foreground color
```

### `Code`
```python
rc.Code(code="print('hello')", language="python", inline=False, show_line_numbers=True)
rc.Code(code="x = 1", inline=True)   # inline code span
```

### `Link`
```python
rc.Link(text="Visit Docs", href="/docs", target="_self")
rc.Link(text="GitHub", href="https://github.com", external=True, target="_blank")
```

### `BlockQuote`
```python
rc.BlockQuote(children=[rc.Text("The only way to do great work is to love what you do.")])
```

### `Markdown`
Renders a Markdown string as rich HTML. Requires `preloaded_features=["markdown"]`.
```python
rc.Markdown("# Hello\n\nThis is **bold** and _italic_.")
rc.Markdown(id="output", content="")   # start empty for streaming
```

### `Separator`
```python
rc.Separator()                              # horizontal divider
rc.Separator(orientation="vertical", class_name="h-6")
```

---

## 4. Button Components

### `Button`
```python
rc.Button(
    label="Click Me",
    variant="default",       # "default"|"secondary"|"destructive"|"outline"|"ghost"|"link"
    size="md",               # "xs"|"sm"|"md"|"lg"|"xl"
    icon="save",             # Lucide icon name (optional)
    icon_position="left",    # "left"|"right"
    disabled=False,
    loading=False,           # shows spinner, disables button
    type="button",           # "button"|"submit"|"reset"
    on_click=ctx.callback(handler),
)
```

### `IconButton`
Square icon-only button.
```python
rc.IconButton(
    icon="trash",
    variant="ghost",
    size="md",
    disabled=False,
    aria_label="Delete item",
    on_click=ctx.callback(handler),
)
```

---

## 5. Input Components

### `Input`
```python
rc.Input(
    name="email",
    label="Email Address",
    description="We'll never share your email.",
    type="email",            # "text"|"email"|"password"|"number"|"tel"|"url"|"search"
    placeholder="you@example.com",
    value=None,              # controlled value (None = uncontrolled)
    default_value=None,
    required=True,
    disabled=False,
    read_only=False,
    error="Invalid email",   # shown below input
    debounce=300,            # ms delay before on_change fires
    on_change=ctx.callback(handler),
    on_blur=ctx.callback(handler),
    on_focus=ctx.callback(handler),
    on_keydown=ctx.callback(handler),
)
```

### `Textarea`
```python
rc.Textarea(
    name="bio",
    label="Biography",
    placeholder="Tell us about yourself…",
    rows=5,
    debounce=300,
    on_change=ctx.callback(handler),
)
```

### `Select`
```python
rc.Select(
    name="country",
    label="Country",
    options=[
        {"value": "us", "label": "United States"},
        {"value": "de", "label": "Germany", "disabled": True},
    ],
    value=None,              # controlled
    placeholder="Choose…",
    required=True,
    error=None,
    on_change=ctx.callback(handler),
)
```

### `Checkbox`
```python
rc.Checkbox(
    name="agree",
    value="yes",
    label="I agree to the terms",
    checked=False,
    required=False,
    on_change=ctx.callback(handler),
)
```

### `CheckboxGroup`
```python
rc.CheckboxGroup(
    name="fruits",
    label="Favourite fruits",
    value=["apple"],         # controlled list
    orientation="vertical",  # "vertical"|"horizontal"
    error=None,
    on_change=ctx.callback(handler),  # ctx.event_data = {"value": ["apple", ...]}
    children=[
        rc.Checkbox(value="apple", label="Apple"),
        rc.Checkbox(value="banana", label="Banana"),
        rc.Checkbox(value="orange", label="Orange", disabled=True),
    ],
)
```

### `RadioGroup` / `Radio`
```python
rc.RadioGroup(
    name="plan",
    label="Select a plan",
    value="pro",             # controlled
    orientation="vertical",
    on_change=ctx.callback(handler),  # ctx.event_data = {"value": "pro"}
    children=[
        rc.Radio(value="free", label="Free"),
        rc.Radio(value="pro", label="Pro"),
    ],
)
```

---

## 6. Form Components

### `Form`
Intercepts submit, routes to server via WebSocket:
```python
rc.Form(
    on_submit=ctx.callback(handle_submit),  # ctx.event_data = form field dict
    children=[
        rc.Input(name="email", label="Email", type="email"),
        rc.Input(name="password", label="Password", type="password"),
        rc.Button("Submit", type="submit"),
    ],
)
```

### `FormField`
```python
rc.FormField(
    label="Password",
    hint="At least 8 characters.",
    required=True,
    error="Too short.",
    children=[rc.Input(name="password", type="password")],
)
```

### `Label`
```python
rc.Label(text="API Key", html_for="api-key-input", required=True)
```

### `InputWrapper`
Wraps any custom control with label/description/error chrome:
```python
rc.InputWrapper(
    label="Volume",
    description="Adjust playback volume.",
    required=True,
    error=None,
    children=[rc.Slider(value=[75], min=0, max=100)],
)
```

---

## 7. Advanced Controls

### `Switch`
```python
rc.Switch(
    checked=True,
    disabled=False,
    name="notifications",
    on_checked_change=ctx.callback(handler),  # ctx.event_data = True/False
)
```

### `Slider`
```python
rc.Slider(
    label="Volume",
    value=[50],              # list[float]; two values = range slider
    min=0, max=100, step=1,
    show_value=True,
    orientation="horizontal",
    on_value_change=ctx.callback(handler),  # ctx.event_data = [50]
    on_value_commit=ctx.callback(handler),  # fires when user releases
)
```

### `Toggle` / `ToggleGroup`
```python
rc.Toggle(
    label="Bold",
    icon="Bold",
    pressed=True,
    on_pressed_change=ctx.callback(handler),
)

rc.ToggleGroup(
    type="multiple",         # "single"|"multiple"
    default_value={"bold": True, "italic": False},
    on_value_change=ctx.callback(handler),
    children=[
        rc.ToggleGroupItem("Bold", icon="Bold", name="bold"),
        rc.ToggleGroupItem("Italic", icon="Italic", name="italic"),
    ],
)
```

### `Calendar` / `DatePicker`
```python
from datetime import date
rc.Calendar(
    mode="single",           # "single"|"multiple"|"range"
    selected=date(2026, 5, 31),
    on_select=ctx.callback(handler),
)

rc.DatePicker(
    value="2026-05-31",      # ISO date string
    placeholder="Pick a date",
    on_change=ctx.callback(handler),
)
```

### `Combobox`
```python
rc.Combobox(
    options=[{"value": "react", "label": "React"}, ...],
    value="react",
    placeholder="Select framework…",
    search_placeholder="Search…",
    on_change=ctx.callback(handler),
)
```

---

## 8. Card Components

```python
# Full composition:
rc.Card(
    id="my-card",
    on_click=ctx.callback(handler),   # makes card interactive
    children=[
        rc.CardHeader(
            title="Dashboard",
            description="Overview",
        ),
        rc.CardContent(children=[rc.Text("Main content")]),
        rc.CardFooter(children=[
            rc.Button("Cancel", variant="outline"),
            rc.Button("Save", on_click=ctx.callback(save)),
        ]),
    ]
)

# Shorthand:
rc.Card(title="Quick Card", description="Subtitle", children=[...])
```

Sub-components: `CardTitle`, `CardDescription`, `CardHeader`, `CardContent`, `CardFooter`.

---

## 9. Data Display Components

### `Table` (low-level, full control)
```python
rc.Table(
    hoverable=True,
    children=[
        rc.TableHeader(children=[
            rc.TableRow(children=[
                rc.TableHead(children=["Name"]),
                rc.TableHead(children=["Email"], class_name="text-right"),
            ])
        ]),
        rc.TableBody(children=[
            rc.TableRow(children=[
                rc.TableCell(children=["Alice"]),
                rc.TableCell(children=["alice@example.com"], class_name="text-right"),
            ]),
        ]),
    ]
)
```

### `DataTable` (batteries included — sorting, filtering, pagination)
```python
rc.DataTable(
    columns=[
        {"key": "id",    "header": "#",     "width": "60px", "align": "right"},
        {"key": "name",  "header": "Name",  "sortable": True},
        {"key": "email", "header": "Email", "sortable": True},
        {"key": "role",  "header": "Role",  "align": "center"},
    ],
    data=[
        {"id": 1, "name": "Alice", "email": "alice@example.com", "role": "Admin"},
        {"id": 2, "name": "Bob",   "email": "bob@example.com",   "role": "Editor"},
    ],
    sortable=True,
    filterable=True,
    paginated=True,
    page_size=10,
    loading=False,
    empty_message="No records found.",
    on_row_click=ctx.callback(handler),       # ctx.event_data = row dict
    on_sort_change=ctx.callback(handler),     # ctx.event_data = {"key": "name", "direction": "asc"}
    on_filter_change=ctx.callback(handler),   # ctx.event_data = {"value": "alice"}
    on_page_change=ctx.callback(handler),     # ctx.event_data = {"page": 2}
)
# Column values can be Component instances (e.g. Badge); they are serialized automatically.
```

### `Badge`
```python
rc.Badge("Active", variant="success")
rc.Badge(children=["New"], icon="star", icon_position="left", size="md")
# variants: "default"|"secondary"|"destructive"|"outline"|"success"|"warning"
# sizes: "xs"|"sm"|"md"|"lg"|"xl"
```

### `Avatar`
```python
rc.Avatar(src="/avatars/alice.jpg", alt="Alice", size="lg")
rc.Avatar(fallback="JD", size="md")   # initials fallback
```

### `Tooltip`
```python
rc.Tooltip(
    content="This cannot be undone.",
    side="top",       # "top"|"right"|"bottom"|"left"
    children=[rc.Button("Delete", variant="destructive")],
)
```

### `Tabs` / `TabItem`
```python
rc.Tabs(
    default_value="overview",
    value=None,                      # controlled
    direction="horizontal",          # "horizontal"|"vertical"
    on_value_change=ctx.callback(handler),
    children=[
        rc.TabItem(value="overview", label="Overview", icon="home",
                   children=[rc.Text("Overview content")]),
        rc.TabItem(value="settings", label="Settings",
                   children=[rc.Text("Settings content")]),
        rc.TabItem(value="disabled", label="Disabled", disabled=True, children=[]),
    ],
)
```

### `Accordion`
```python
rc.Accordion(
    type="single",              # "single"|"multiple"
    collapsible=True,
    default_value="item-1",
    on_value_change=ctx.callback(handler),
    children=[
        rc.AccordionItem(value="item-1", children=[
            rc.AccordionTrigger(children=["Is it accessible?"]),
            rc.AccordionContent(children=[rc.Text("Yes.")]),
        ]),
        rc.AccordionItem(value="item-2", children=[
            rc.AccordionTrigger(children=["Is it styled?"]),
            rc.AccordionContent(children=[rc.Text("Yes.")]),
        ]),
    ],
)
```

### `List` / `ListItem`
```python
rc.List(children=["Apples", "Bananas", "Cherries"])
rc.List(ordered=True, children=["First step", "Second step"])
```

### `Image`
```python
rc.Image(src="/path/to/image.jpg", alt="Description", width=400, height=300)
```

---

## 10. Feedback Components

### `Alert`
```python
rc.Alert(
    title="Heads up!",
    message="Something changed.",
    variant="default",   # "default"|"success"|"warning"|"destructive"|"info"
    dismissible=True,
    on_dismiss=ctx.callback(handler),
)
```

### `Progress`
```python
rc.Progress(
    value=65,
    max=100,
    label="Uploading…",
    show_value=True,
    foreground_color="primary",
    striped="animated",          # None|"static"|"animated"
)
```

### `Spinner`
```python
rc.Spinner(size="md")   # "sm"|"md"|"lg"
```

### `Skeleton`
```python
rc.Skeleton(width="100%", height="1rem", variant="text")
rc.Skeleton(width=40, height=40, circle=True)
```

### `ConnectionStatus`
```python
rc.ConnectionStatus(
    children_connected=[rc.Badge("Online", variant="success")],
    children_disconnected=[rc.Alert(title="Connection Lost", variant="destructive")],
    position="bottom-right",   # "top-left"|"top-right"|"bottom-left"|"bottom-right"|"inline"
    on_disconnect=ctx.callback(handler),
    on_reconnect=ctx.callback(handler),
    debounce_ms=500,
)
```

---

## 11. Overlay Components

### `Dialog`
```python
rc.Dialog(
    open=ctx.state.get("dialog_open", False),
    on_open_change=ctx.callback(on_open_change),
    children=[
        rc.DialogContent(children=[
            rc.DialogHeader(children=[
                rc.DialogTitle("Confirm Deletion"),
                rc.DialogDescription("This cannot be undone."),
            ]),
            rc.DialogFooter(children=[
                rc.Button("Cancel", variant="outline", on_click=ctx.callback(close_dialog)),
                rc.Button("Delete", variant="destructive", on_click=ctx.callback(confirm_delete)),
            ]),
        ]),
    ],
)
```

### `Sheet`
Slide-in panel from an edge:
```python
rc.Sheet(
    open=ctx.state.get("sheet_open", False),
    on_open_change=ctx.callback(handle_open),
    side="right",        # "top"|"right"|"bottom"|"left"
    children=[
        rc.SheetContent(children=[
            rc.SheetHeader(children=[rc.SheetTitle("Settings")]),
            rc.Container(children=[...form...]),
        ]),
    ],
)
```

### `Popover`
```python
rc.Popover(
    children=[
        rc.PopoverTrigger(children=[rc.Button("Open")]),
        rc.PopoverContent(children=[rc.Text("Popover content")]),
    ]
)
```

### `DropdownMenu`
```python
rc.DropdownMenu(children=[
    rc.DropdownMenuTrigger(children=[rc.Button("Options")]),
    rc.DropdownMenuContent(children=[
        rc.DropdownMenuLabel(label="Actions"),
        rc.DropdownMenuSeparator(),
        rc.DropdownMenuItem(label="Edit", icon="pencil", on_click=ctx.callback(handler)),
        rc.DropdownMenuItem(label="Delete", icon="trash", on_click=ctx.callback(handler)),
    ]),
])
```

---

## 12. Scroll Area

```python
rc.ScrollArea(
    id="scroll-area",
    class_name="border rounded-lg p-4",
    style={"height": "500px"},
    stick_to_bottom=True,   # auto-scrolls to new content (for streaming/chat)
    children=[rc.Markdown(id="output", content="")],
)
```

`stick_to_bottom` auto-scrolls unless the user has scrolled up; re-sticks when they scroll back to the bottom.

---

## 13. Resizable Panels

```python
rc.ResizablePanelGroup(
    direction="horizontal",   # "horizontal"|"vertical"
    children=[
        rc.ResizablePanel(
            default_size=25, min_size=15, max_size=40,
            children=[rc.Text("Left panel")],
        ),
        rc.ResizableHandle(with_handle=True),
        rc.ResizablePanel(
            default_size=75,
            children=[rc.Text("Main content")],
        ),
    ],
)
```

---

## 14. Collapsible

```python
rc.Collapsible(
    default_open=True,
    open=None,                # controlled
    on_open_change=ctx.callback(handler),
    children=[
        rc.CollapsibleTrigger(children=[rc.Button("Toggle Section")]),
        rc.CollapsibleContent(children=[rc.Text("Hidden content")]),
    ],
)
```

---

## Lazy-Loading Feature Bundles

Heavy components require their feature chunk to be loaded. Pass the chunk name(s) to `preloaded_features` on `RefastApp`:

```python
ui = RefastApp(
    title="My App",
    preloaded_features=["charts", "markdown", "icons"],
)
```

| Feature | Components |
|---------|-----------|
| `"charts"` | Chart components (ECharts extension etc.) |
| `"markdown"` | `Markdown` component |
| `"icons"` | Lucide icon rendering in all components |
| `"navigation"` | Sidebar, Menubar, NavigationMenu, Command |
| `"overlay"` | Dialog, Sheet, Popover, DropdownMenu |
| `"controls"` | Slider, Calendar, DatePicker, Combobox, InputOTP |

Omit `preloaded_features` to load everything (default). Pass `[]` for minimal bundle (core only).
