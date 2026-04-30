"""File Uploads & Downloads — /docs/concepts/file-transfers."""

import csv
import io
from datetime import datetime

from refast import Context
from refast.components import (
    Alert,
    Badge,
    Button,
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
    Column,
    Container,
    FileUploader,
    Heading,
    Image,
    Markdown,
    Row,
    Separator,
    Text,
)

PAGE_TITLE = "File Uploads & Downloads"
PAGE_ROUTE = "/docs/concepts/file-transfers"

# ── Demo: Image uploader ─────────────────────────────────────────────────────


async def _demo_on_image_uploaded(ctx: Context):
    files = ctx.event_data.get("files", [])
    if not files:
        return
    first = files[0]
    ctx.state.set("demo_image_url", f"/api/file/{first['id']}")
    ctx.state.set("demo_image_name", first["name"])
    ctx.state.set("demo_image_error", None)
    await ctx.refresh()


async def _demo_on_image_error(ctx: Context):
    ctx.state.set("demo_image_error", ctx.event_data.get("error", "Upload failed"))
    await ctx.refresh()


# ── Demo: Programmatic download ──────────────────────────────────────────────

_SAMPLE_DATA = [
    {"Name": "Alice", "Department": "Engineering", "Salary": "95000"},
    {"Name": "Bob", "Department": "Design", "Salary": "82000"},
    {"Name": "Carol", "Department": "Product", "Salary": "110000"},
]


async def _demo_download_csv(ctx: Context):
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=["Name", "Department", "Salary"])
    writer.writeheader()
    writer.writerows(_SAMPLE_DATA)
    csv_bytes = buf.getvalue().encode("utf-8")
    filename = f"employees_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    url = await ctx.create_file_url(csv_bytes, filename, "text/csv")
    await ctx.trigger_download(url, filename)


# ── Demo: Inline image generation ────────────────────────────────────────────

_SWATCHES = [
    ("#2563eb", "Blue"),
    ("#16a34a", "Green"),
    ("#dc2626", "Red"),
    ("#9333ea", "Purple"),
]


def _make_swatch_svg(color: str, label: str) -> bytes:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="200" height="100">'
        f'<rect width="200" height="100" fill="{color}"/>'
        f'<text x="100" y="58" font-size="18" font-family="sans-serif" '
        f'text-anchor="middle" fill="white" font-weight="bold">{label}</text>'
        f"</svg>"
    ).encode()


async def _demo_show_swatch(ctx: Context, color: str, label: str):
    svg_bytes = _make_swatch_svg(color, label)
    url = await ctx.create_file_url(svg_bytes, f"{label}.svg", "image/svg+xml", inline=True)
    ctx.state.set("demo_swatch_url", url)
    ctx.state.set("demo_swatch_label", label)
    await ctx.refresh()


# ── Page renderer ────────────────────────────────────────────────────────────


def render(ctx: Context):
    """Render the file transfers concept page."""
    from docs_site.app import docs_layout

    content = Container(
        class_name="max-w-4xl mx-auto p-6 space-y-8",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            Markdown(content=INTRO_CONTENT),
            _demo_uploader_card(ctx),
            Markdown(content=UPLOAD_REFERENCE),
            _demo_download_card(ctx),
            Markdown(content=DOWNLOAD_REFERENCE),
            _demo_inline_url_card(ctx),
            Markdown(content=INLINE_URL_REFERENCE),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


# ── Live demo sections ───────────────────────────────────────────────────────


def _demo_uploader_card(ctx: Context):
    image_url = ctx.state.get("demo_image_url")
    image_name = ctx.state.get("demo_image_name")
    image_error = ctx.state.get("demo_image_error")

    return Card(
        children=[
            CardHeader(
                children=[
                    CardTitle("Live Demo — Image Uploader"),
                    CardDescription("Drop an image (PNG, JPG, GIF, WebP — max 5 MB)."),
                ]
            ),
            CardContent(
                class_name="space-y-4",
                children=[
                    FileUploader(
                        label="Drop an image here",
                        description="PNG, JPG, GIF, WebP – max 5 MB",
                        variant="dropzone",
                        accept="image/*",
                        max_size=5 * 1024 * 1024,
                        on_upload_complete=ctx.callback(_demo_on_image_uploaded),
                        on_upload_error=ctx.callback(_demo_on_image_error),
                    ),
                    *([Alert(image_error, variant="destructive")] if image_error else []),
                    *(
                        [
                            Column(
                                class_name="items-center gap-2",
                                children=[
                                    Text(
                                        f"Uploaded: {image_name}",
                                        class_name="text-sm font-medium",
                                    ),
                                    Image(
                                        src=image_url,
                                        alt=image_name or "",
                                        class_name="max-h-64 rounded-md border",
                                    ),
                                ],
                            )
                        ]
                        if image_url
                        else []
                    ),
                ],
            ),
        ]
    )


def _demo_download_card(ctx: Context):
    return Card(
        children=[
            CardHeader(
                children=[
                    CardTitle("Live Demo — Programmatic Download"),
                    CardDescription(
                        "Generates a CSV in memory and triggers a browser download."
                    ),
                ]
            ),
            CardContent(
                children=[
                    Button(
                        "Download Employee CSV",
                        on_click=ctx.callback(_demo_download_csv),
                        variant="outline",
                        icon="download",
                    ),
                ]
            ),
        ]
    )


def _demo_inline_url_card(ctx: Context):
    swatch_url = ctx.state.get("demo_swatch_url")
    swatch_label = ctx.state.get("demo_swatch_label")

    return Card(
        children=[
            CardHeader(
                children=[
                    CardTitle("Live Demo — Inline File URL"),
                    CardDescription(
                        "Generates SVG bytes on the server and displays them inline "
                        "without triggering a download."
                    ),
                ]
            ),
            CardContent(
                class_name="space-y-4",
                children=[
                    Row(
                        class_name="gap-2 flex-wrap",
                        children=[
                            Button(
                                label,
                                on_click=ctx.callback(
                                    _demo_show_swatch, color=color, label=label
                                ),
                                variant="outline",
                            )
                            for color, label in _SWATCHES
                        ],
                    ),
                    *(
                        [
                            Column(
                                class_name="items-center gap-2",
                                children=[
                                    Text(
                                        f"Swatch: {swatch_label}",
                                        class_name="text-sm font-medium",
                                    ),
                                    Image(
                                        src=swatch_url,
                                        alt=swatch_label or "",
                                        class_name="rounded-md border",
                                    ),
                                ],
                            )
                        ]
                        if swatch_url
                        else []
                    ),
                ],
            ),
        ]
    )


# ── Page content ─────────────────────────────────────────────────────────────

INTRO_CONTENT = r"""
Refast provides first-class support for file uploads from the browser and
programmatic file downloads triggered from server callbacks.

## Upload Flow

```
Browser → FileUploader → /api/upload → callback(ctx)
```

The `FileUploader` component handles chunked upload, progress reporting, and drag-and-drop.
Your Python callback receives file metadata via `ctx.event_data` and can read the uploaded
bytes via the returned file ID.

## Download Flow

```
Python callback → ctx.create_file_url() → ctx.trigger_download()
```

Your callback generates data in memory, registers it as a temporary file URL, then instructs
the browser to download it — all without any extra HTTP endpoints.
"""

UPLOAD_REFERENCE = r"""
## FileUploader

```python
from refast.components import FileUploader

FileUploader(
    label="Drop files here",
    description="PDF, PNG up to 10 MB",
    variant="dropzone",           # "dropzone" (default) or "button"
    accept="image/*",             # MIME type filter (optional)
    multiple=False,               # Allow multiple file selection
    max_files=5,                  # Max number of files (when multiple=True)
    max_size=10 * 1024 * 1024,    # Max file size in bytes
    drag_drop=True,               # Enable drag-and-drop (button variant)
    on_select=ctx.callback(on_select),                          # Files selected
    on_upload_complete=ctx.callback(on_done),                   # Upload finished
    on_upload_error=ctx.callback(on_error),                     # Upload failed
    on_remove=ctx.callback(on_removed),                         # File removed from list
)
```

### Callback event data shapes

| Callback | `ctx.event_data` keys |
|---|---|
| `on_select` | `{"files": [{id, name, size, content_type}]}` |
| `on_upload_complete` | `{"files": [{id, name, size, content_type}]}` |
| `on_upload_error` | `{"error": "message", "file": {name, ...}}` |
| `on_remove` | `{"file": {name, size, ...}}` |

### Reading uploaded file contents

Use the `id` from `ctx.event_data["files"][0]["id"]` to build a URL:

```python
async def on_done(ctx: Context):
    files = ctx.event_data.get("files", [])
    for f in files:
        file_url = f"/api/file/{f['id']}"   # served by Refast automatically
        ctx.state.set("url", file_url)
    await ctx.refresh()
```

The URL is served by Refast with the correct `Content-Type` header. Use it in an
`Image` component or any other place that accepts a URL.
"""

DOWNLOAD_REFERENCE = r"""
## ctx.create_file_url()

Register in-memory bytes as a temporary file that can be downloaded or displayed inline.

```python
url = await ctx.create_file_url(
    data,             # bytes
    filename,         # str — suggested download filename
    content_type,     # str — MIME type, e.g. "text/csv", "application/pdf"
    inline=False,     # True → Content-Disposition: inline (for display, not download)
)
```

The URL is scoped to the current session and cleaned up automatically after a short TTL.

### Example — generate and download a CSV

```python
import csv, io
from datetime import datetime

async def download_report(ctx: Context):
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=["Name", "Score"])
    writer.writeheader()
    writer.writerows([{"Name": "Alice", "Score": 95}, {"Name": "Bob", "Score": 82}])

    filename = f"report_{datetime.now().strftime('%Y%m%d')}.csv"
    url = await ctx.create_file_url(buf.getvalue().encode(), filename, "text/csv")
    await ctx.trigger_download(url, filename)
```

## ctx.trigger_download()

Instruct the browser to download a URL as a file. Works with any URL — including
ones created with `ctx.create_file_url()`.

```python
await ctx.trigger_download(
    url,       # str — the URL to download
    filename,  # str — the filename that will appear in the browser's download dialog
)
```

### Supported file types

Any MIME type that `bytes` can represent works: CSV, JSON, PDF, images, ZIP archives, etc.

```python
# PDF
url = await ctx.create_file_url(pdf_bytes, "report.pdf", "application/pdf")

# JSON
import json
url = await ctx.create_file_url(
    json.dumps(data).encode(), "data.json", "application/json"
)

# ZIP
url = await ctx.create_file_url(zip_bytes, "export.zip", "application/zip")
```
"""

INLINE_URL_REFERENCE = r"""
## Inline display (no download prompt)

Pass `inline=True` to `ctx.create_file_url()` to get a URL you can use directly as
an image `src` or link `href` without triggering a browser download dialog.

```python
async def show_generated_image(ctx: Context):
    png_bytes = render_chart_to_png(...)  # your rendering logic
    url = await ctx.create_file_url(png_bytes, "chart.png", "image/png", inline=True)
    ctx.state.set("chart_url", url)
    await ctx.refresh()

# In the page renderer:
Image(src=ctx.state.get("chart_url", ""), alt="Generated chart")
```

| `inline` | `Content-Disposition` | Use case |
|---|---|---|
| `False` (default) | `attachment` | Browser download dialog |
| `True` | `inline` | Display in `<img>`, `<a>`, etc. |

## See Also

- [DOM Updates](/docs/concepts/updates) — Other ways to update the UI
- [Streaming](/docs/concepts/streaming) — Incremental content delivery
- [Form Inputs](/docs/components/inputs) — Other input components
"""
