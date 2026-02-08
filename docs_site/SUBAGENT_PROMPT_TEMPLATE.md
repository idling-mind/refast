# Refast Docs — Sub-Agent Prompt Template

Use this template when dispatching sub-agents to write individual documentation pages.
Copy the template below and fill in the `{{...}}` placeholders for the specific page.

---

## Template

```
You are writing documentation for the **Refast** framework — a Python + React UI framework
built on FastAPI. The documentation site is itself built with Refast (dogfooding).

## Your Task

Write the complete content for the **{{PAGE_TITLE}}** documentation page.

- **File to edit:** `docs_site/pages/{{SECTION}}/{{FILENAME}}.py`
- **Route:** `{{PAGE_ROUTE}}`
- **Section:** {{SECTION_NAME}}

## What to Do

1. **Read these files first** (use read_file tool) to understand the feature being documented:
{{SOURCE_FILES_LIST}}

2. **Read the section instructions** for detailed content requirements:
   - `docs_site/pages/{{SECTION}}/AGENT_INSTRUCTIONS.md`

3. **Read one or two existing completed pages** as style references:
   - `docs_site/pages/getting_started/installation.py`
   - `docs_site/pages/home.py`

4. **Read the target file** you're editing to see the current placeholder:
   - `docs_site/pages/{{SECTION}}/{{FILENAME}}.py`

5. **Write the page** by replacing the CONTENT string and optionally the render()
   function with full documentation content.

## Page Structure Rules

Every page module MUST follow this pattern:

```python
"""{{PAGE_TITLE}} — {{PAGE_ROUTE}}."""

from refast.components import (
    # Only import what you actually use
    Container,
    Heading,
    Markdown,
    Separator,
    # Add more as needed for live demos: Button, Card, Row, Column, etc.
)

PAGE_TITLE = "{{PAGE_TITLE}}"
PAGE_ROUTE = "{{PAGE_ROUTE}}"

def render(ctx):
    """Render the {{page description}} page."""
    from docs_site.app import docs_layout  # MUST be deferred import

    content = Container(
        class_name="max-w-4xl mx-auto p-6",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            Markdown(content=CONTENT),
            # Optional: live demos with real components below the markdown
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)

CONTENT = r"""
... full page content here ...
"""
```

## Content Writing Guidelines

### Prose & Markdown
- Use `Markdown(content=CONTENT)` for all prose, tables, and code blocks.
- Use `r"""..."""` raw strings for the CONTENT to avoid backslash issues.
- Use GFM (GitHub Flavored Markdown): tables, strikethrough, task lists.
- Code blocks with triple-backtick + language tag for syntax highlighting.
- Cross-reference other pages using markdown links: `[State](/docs/concepts/state)`.

### Structure Each Page As
1. **Intro paragraph** — What is this, why does it matter (2-3 sentences).
2. **Basic Usage** — Simplest working example with code block.
3. **Detailed API / Props Table** — All parameters, types, defaults.
4. **Patterns & Examples** — Common usage patterns, each with a code block.
5. **Notes / Gotchas** — Edge cases, limitations, tips.
6. **Next Steps** — Links to 2-3 related pages.

### Props Tables Format
```markdown
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `str` | — | Button text |
| `variant` | `"default" \| "outline"` | `"default"` | Visual style |
| `on_click` | `Callback \| None` | `None` | Click handler |
```

### Live Demos (Component Reference Pages)
For component reference pages, include actual rendered components alongside code:

```python
def render(ctx):
    from docs_site.app import docs_layout

    content = Container(
        class_name="max-w-4xl mx-auto p-6",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            Markdown(content=INTRO_CONTENT),

            # Live demo section
            Heading("Live Examples", level=2),
            Card(
                class_name="p-4",
                children=[
                    Row(gap=3, children=[
                        Button("Default"),
                        Button("Secondary", variant="secondary"),
                        Button("Destructive", variant="destructive"),
                    ]),
                ],
            ),

            Markdown(content=REST_OF_CONTENT),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)
```

### Callouts
Use Alert components for important notes:
```python
Alert(title="Note", description="State is only available in WebSocket context.")
```

Or use blockquotes in Markdown:
```markdown
> **Note:** State is only available within callback/WebSocket context.
```

## Component Defaults to Know

- `Row`, `Column`, `Flex` default to `gap=2` (0.5rem spacing)
- `Grid` defaults to `gap=4` (1rem spacing)
- Cards have internal padding (`p-6`) but no external margin
- Use `class_name="my-4"` or similar for spacing between sections

## Available Components

From `refast.components`:
Container, Flex, Row, Column, Grid, Center, Heading, Text, Paragraph, Code,
Link, Markdown, Badge, Icon, Button, IconButton, Card, CardHeader, CardTitle,
CardDescription, CardContent, CardFooter, Tabs, TabItem, Accordion,
AccordionItem, Alert, Separator, Table, TableHeader, TableBody, TableRow,
TableHead, TableCell, Input, Textarea, Select, SelectItem, Checkbox, Switch,
RadioGroup, RadioGroupItem, Slider, Toggle, ToggleGroup, ToggleGroupItem,
Dialog, DialogTrigger, DialogContent, DialogHeader, DialogTitle,
DialogDescription, DialogFooter, Sheet, SheetTrigger, SheetContent,
DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem,
Breadcrumb, BreadcrumbItem, BreadcrumbLink, BreadcrumbList, BreadcrumbPage,
BreadcrumbSeparator, Pagination, PaginationContent, PaginationItem,
PaginationLink, PaginationNext, PaginationPrevious, NavigationMenu,
NavigationMenuList, NavigationMenuItem, NavigationMenuTrigger,
NavigationMenuContent, NavigationMenuLink, BarChart, LineChart, AreaChart,
PieChart, RadarChart, RadialChart, Label, Kbd, AspectRatio, ScrollArea,
ResizablePanelGroup, ResizablePanel, ResizableHandle, Collapsible,
CollapsibleTrigger, CollapsibleContent, Progress, Spinner, Skeleton,
Image, Avatar, Tooltip

## Quality Checklist

Before finishing, verify:
- [ ] No `> **TODO**` markers remain in the content
- [ ] All code examples are syntactically correct Python
- [ ] All imports in the module are used
- [ ] Cross-links use correct routes (e.g., `/docs/concepts/state`, not `/state`)
- [ ] Props tables list ALL public props for each documented component
- [ ] The page reads well as a standalone document
- [ ] Content is technically accurate (based on the source files you read)

## DO NOT

- Do NOT invent APIs or props that don't exist in the source code
- Do NOT use components that aren't in the framework
- Do NOT add navigation callbacks unless the page needs internal links
- Do NOT change PAGE_ROUTE or PAGE_TITLE (they must match app.py's NAV_SECTIONS)
- Do NOT modify docs_site/app.py
```

---

## Example: Filling In the Template

For the **State Management** concept page:

```
{{PAGE_TITLE}}       = State Management
{{SECTION}}          = concepts
{{FILENAME}}         = state
{{PAGE_ROUTE}}       = /docs/concepts/state
{{SECTION_NAME}}     = Core Concepts
{{SOURCE_FILES_LIST}} =
   - `src/refast/state.py` — State and StateManager classes
   - `src/refast/context.py` — How ctx.state is accessed
   - `examples/basic/app.py` — Counter example using state
   - `examples/todo_app/app.py` — Todo example using state
```

For the **Buttons & Actions** component reference page:

```
{{PAGE_TITLE}}       = Buttons & Actions
{{SECTION}}          = components
{{FILENAME}}         = buttons
{{PAGE_ROUTE}}       = /docs/components/buttons
{{SECTION_NAME}}     = Components
{{SOURCE_FILES_LIST}} =
   - `src/refast/components/shadcn/button.py` — Button, IconButton Python classes
   - `src/refast/components/shadcn/controls.py` — Toggle, ToggleGroup
   - `src/refast/components/shadcn/overlay.py` — DropdownMenu and subcomponents
   - `src/refast-client/src/components/shadcn/Button.tsx` — React renderer (variants, sizes)
```

---

## Quick Reference: All Pages

| Section | File | Route | Key Source Files |
|---------|------|-------|-----------------|
| Getting Started | `installation.py` | `/docs/getting-started` | `examples/hello.py`, `src/refast/app.py`, `pyproject.toml` |
| Getting Started | `architecture.py` | `/docs/architecture` | `src/refast/app.py`, `src/refast/router.py`, `src/refast/context.py` |
| Getting Started | `quick_tour.py` | `/docs/quick-tour` | `examples/todo_app/app.py` |
| Getting Started | `examples_gallery.py` | `/docs/examples` | All `examples/*/app.py` and `examples/*/README.md` |
| Concepts | `components.py` | `/docs/concepts/components` | `src/refast/components/base.py`, `src/refast/components/registry.py` |
| Concepts | `callbacks.py` | `/docs/concepts/callbacks` | `src/refast/context.py`, `src/refast/events/types.py` |
| Concepts | `state.py` | `/docs/concepts/state` | `src/refast/state.py`, `src/refast/context.py` |
| Concepts | `store.py` | `/docs/concepts/store` | `src/refast/store.py`, `docs/PROP_STORE_GUIDE.md` |
| Concepts | `updates.py` | `/docs/concepts/updates` | `src/refast/context.py`, `examples/longrunning.py` |
| Concepts | `routing.py` | `/docs/concepts/routing` | `src/refast/app.py`, `src/refast/router.py`, `examples/multi_page/app.py` |
| Concepts | `streaming.py` | `/docs/concepts/streaming` | `src/refast/events/stream.py`, `docs/STREAMING_GUIDE.md`, `examples/streaming/app.py` |
| Concepts | `background.py` | `/docs/concepts/background` | `src/refast/context.py`, `examples/longrunning.py`, `examples/realtime_dashboard/app.py` |
| Concepts | `theming.py` | `/docs/concepts/theming` | `src/refast/theme/`, `examples/theme_showcase/app.py` |
| Concepts | `toasts.py` | `/docs/concepts/toasts` | `src/refast/context.py`, `examples/toast_showcase/app.py` |
| Concepts | `js_interop.py` | `/docs/concepts/js-interop` | `src/refast/context.py`, `examples/js_callbacks/app.py` |
| Components | `layout.py` | `/docs/components/layout` | `src/refast/components/base.py`, `src/refast/components/shadcn/layout.py` |
| Components | `typography.py` | `/docs/components/typography` | `src/refast/components/shadcn/typography.py` |
| Components | `buttons.py` | `/docs/components/buttons` | `src/refast/components/shadcn/button.py`, `src/refast/components/shadcn/controls.py` |
| Components | `inputs.py` | `/docs/components/inputs` | `src/refast/components/shadcn/input.py`, `src/refast/components/shadcn/form.py` |
| Components | `cards.py` | `/docs/components/cards` | `src/refast/components/shadcn/card.py` |
| Components | `data_display.py` | `/docs/components/data-display` | `src/refast/components/shadcn/data_display.py` |
| Components | `navigation.py` | `/docs/components/navigation` | `src/refast/components/shadcn/navigation.py`, `src/refast/components/shadcn/sidebar.py` |
| Components | `feedback.py` | `/docs/components/feedback` | `src/refast/components/shadcn/feedback.py`, `src/refast/components/shadcn/overlay.py` |
| Components | `charts.py` | `/docs/components/charts` | `src/refast/components/shadcn/chart.py` |
| Components | `utility.py` | `/docs/components/utility` | `src/refast/components/shadcn/icon.py`, `src/refast/components/shadcn/separator.py` |
| Advanced | `component_dev.py` | `/docs/advanced/component-dev` | `docs/COMPONENT_DEVELOPMENT.md`, `docs/NAMING_CONVENTIONS.md` |
| Advanced | `extension_dev.py` | `/docs/advanced/extension-dev` | `docs/EXTENSION_DEVELOPMENT.md` |
| Advanced | `security.py` | `/docs/advanced/security` | `src/refast/security/*.py` |
| Advanced | `sessions.py` | `/docs/advanced/sessions` | `src/refast/session/*.py` |
| Advanced | `styling.py` | `/docs/advanced/styling` | `docs/STYLING_GUIDE.md`, `docs/TAILWIND_SUPPORT.md` |
