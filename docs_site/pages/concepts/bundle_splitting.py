"""Bundle Splitting & Lazy Loading — /docs/concepts/bundle-splitting."""

from refast import Context
from refast.components import (
    Badge,
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
    Column,
    Container,
    Heading,
    Markdown,
    Row,
    Separator,
    Text,
)

PAGE_TITLE = "Bundle Splitting & Lazy Loading"
PAGE_ROUTE = "/docs/concepts/bundle-splitting"


def render(ctx: Context):
    """Render the bundle splitting concept page."""
    from docs_site.app import docs_layout

    content = Container(
        class_name="max-w-4xl mx-auto p-6 space-y-8",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            Markdown(content=CONTENT),
            _feature_table_card(),
            Markdown(content=CONTENT_AFTER_TABLE),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


def _feature_table_card():
    """Visual reference card for all available feature chunks."""
    rows = [
        ("charts", "recharts + all chart wrappers", "refast-charts-*.js", "~180 kB"),
        ("navigation", "Menubar, NavigationMenu, Command palette", "refast-navigation-*.js", "~45 kB"),
        ("overlay", "Dialog, Sheet, Drawer, Popover, HoverCard", "refast-overlay-*.js", "~55 kB"),
        ("controls", "Slider, DatePicker, Combobox, ToggleGroup, Carousel", "refast-controls-*.js", "~70 kB"),
        ("markdown", "Markdown renderer (remark/rehype + syntax highlighting)", "refast-markdown-*.js", "~95 kB"),
        ("katex", "KaTeX math rendering (remark-math, rehype-katex)", "refast-katex-*.js", "~50 kB"),
        ("mermaid", "Mermaid diagramming library", "refast-mermaid-*.js", "~140 kB"),
        ("icons", "Full Lucide icon set (thousands of icons)", "refast-icons-*.js", "~120 kB"),
    ]

    header = Row(
        class_name="grid grid-cols-4 gap-4 px-4 py-2 bg-muted rounded-t-md",
        children=[
            Text("Feature name", class_name="text-sm font-semibold"),
            Text("What it includes", class_name="text-sm font-semibold"),
            Text("Chunk file", class_name="text-sm font-semibold"),
            Text("Approx. size", class_name="text-sm font-semibold"),
        ],
    )

    body_rows = [
        Row(
            class_name="grid grid-cols-4 gap-4 px-4 py-2 border-t",
            children=[
                Badge(name, variant="outline", class_name="font-mono text-xs w-fit"),
                Text(includes, class_name="text-sm"),
                Text(chunk, class_name="text-sm font-mono text-muted-foreground"),
                Text(size, class_name="text-sm text-muted-foreground"),
            ],
        )
        for name, includes, chunk, size in rows
    ]

    return Card(
        children=[
            CardHeader(
                children=[
                    CardTitle("Available Feature Chunks"),
                    CardDescription(
                        "Sizes are approximate gzipped values. "
                        "Actual sizes depend on the build version."
                    ),
                ]
            ),
            CardContent(
                class_name="p-0",
                children=[
                    Column(children=[header, *body_rows]),
                ],
            ),
        ]
    )


CONTENT = r"""
Refast's frontend is split into a small always-loaded **core bundle** and a set of
optional **feature chunks**. By default **no** feature chunks are preloaded — they
load on demand the first time a component from that chunk is rendered. The
`preloaded_features` parameter on `RefastApp` controls which chunks are eagerly
sent to the browser on the initial page load.

## Why it matters

Heavy components like recharts (~180 kB gzipped) or the full Lucide icon set
(~120 kB) add real cost to your initial page load. If a page doesn't use charts
there's no reason to make users download that code.

## The preloaded_features parameter

```python
from refast import RefastApp

# Default — no feature chunks preloaded; all load on demand
app = RefastApp(title="My App")

# Charts only — the recharts chunk is preloaded at startup
app = RefastApp(title="My App", preloaded_features=["charts"])

# All features preloaded — biggest initial bundle, no on-demand loading
app = RefastApp(title="My App", preloaded_features=["charts", "markdown", "katex", "mermaid", "icons", "navigation", "overlay", "controls"])

# Explicitly empty — same as the default, confirms no chunks are preloaded
app = RefastApp(title="My App", preloaded_features=[])
```

Chunks **not** listed in `preloaded_features` are still downloaded the first time
a component from that chunk is rendered — the difference is *when* the download
happens (initial load vs. on demand).

## Always-loaded core components

The following are **always** available regardless of `preloaded_features`:

- Layout: `Container`, `Row`, `Column`, `Grid`, `Flex`, `Separator`
- Typography: `Heading`, `Paragraph`, `Text`, `Code`, `Link`
- Inputs: `Button`, `Input`, `Textarea`, `Select`, `Checkbox`, `Switch`
- Feedback: `Alert`, `Badge`, `Progress`, `Spinner`, `Toast`
- Display: `Card` family, `Table` primitives, `Tabs`, `Accordion`, `Avatar`, `Image`
- Navigation: `Breadcrumb`, `Sidebar` family, `Pagination`

## Feature chunks

The table below lists every available feature name and what it contains.
"""

CONTENT_AFTER_TABLE = r"""
## Choosing the right configuration

| App type | Recommended `preloaded_features` |
|---|---|
| Dashboard with charts | `["charts"]` |
| Admin panel with rich forms | `["controls", "overlay"]` |
| Documentation or content site | `["markdown", "katex", "mermaid", "icons", "navigation"]` |
| Minimal UI / internal tool | `[]` or `None` (default — on demand) |
| Full-featured app | `["charts", "markdown", "katex", "mermaid", "icons", "navigation", "overlay", "controls"]` |

## Example

```python
from refast import RefastApp

# A documentation site — needs markdown rendering, icons, and navigation menus
ui = RefastApp(
    title="My Docs",
    preloaded_features=["markdown", "icons", "navigation"],
)
```

## Measuring the impact

Use your browser's DevTools **Network** tab filtered to **JS** requests. With the default
configuration you will see several `refast-*-*.js` files; with `preloaded_features=[]`
only `refast-client.js` loads on the first request.

```bash
# Run three instances side-by-side to compare (see examples/lazy_loading/)
uvicorn examples.lazy_loading.app:app_all     --port 8001
uvicorn examples.lazy_loading.app:app_charts  --port 8002
uvicorn examples.lazy_loading.app:app_minimal --port 8003
```

## Important notes

- Setting `preloaded_features=[]` does **not** disable any component — it only changes
  when the browser fetches its code (on demand rather than upfront).
- Components from un-preloaded chunks may show a brief loading flash on first render
  while the chunk is being fetched. This is usually imperceptible on a local network
  but can be noticeable over slow connections.
- Use browser caching headers to ensure chunks are only downloaded once per deployment.

## See Also

- [Architecture](/docs/architecture) — How the frontend client works
- [Installation](/docs/getting-started) — Setting up a Refast app
"""
