"""File Transfer Example – FileUploader + programmatic download.

Demonstrates:
1. Dropzone uploader – upload an image, display it inline after upload
2. Button-variant multi-file uploader with progress & validation feedback
3. Dynamic CSV generation + programmatic download via ctx.trigger_download()
4. Inline image generation + display via ctx.create_file_url(inline=True)
5. on_upload_progress with throttle to avoid flooding the server
"""

import csv
import io
import json
from datetime import datetime
from typing import Any

from fastapi import FastAPI

from refast import Context, RefastApp
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
    Paragraph,
    Row,
    Separator,
    Text,
)

# ─── App setup ───────────────────────────────────────────────────────────────

ui = RefastApp(title="File Transfer Demo")

# ─── Section 1: Image uploader (dropzone) ────────────────────────────────────


async def on_image_uploaded(ctx: Context):
    """Called when an image finishes uploading. Display it inline."""
    data = ctx.event_data  # {"files": [{id, name, size, content_type}]}
    files = data.get("files", [])
    if not files:
        return

    first = files[0]
    file_id = first["id"]
    # Build the download URL served by Refast (Content-Disposition: attachment)
    # For display we want inline mode — store a fresh reference in state
    file_url = f"/api/file/{file_id}"
    ctx.state.set("uploaded_image_url", file_url)
    ctx.state.set("uploaded_image_name", first["name"])
    await ctx.refresh()


async def on_image_upload_error(ctx: Context):
    """Show server-side error message for image uploader."""
    error = ctx.event_data.get("error", "Unknown error")
    ctx.state.set("image_error", error)
    await ctx.refresh()


# ─── Section 2: Multi-file uploader with progress ────────────────────────────


async def on_files_selected(ctx: Context):
    """Record how many files were selected."""
    files = ctx.event_data.get("files", [])
    ctx.state.set("selected_count", len(files))
    await ctx.refresh()


async def on_files_progress(ctx: Context):
    """Update progress display for multi-file uploader (throttled)."""
    data = ctx.event_data
    ctx.state.set(
        "upload_progress",
        {
            "file": data.get("file", {}).get("name", ""),
            "percent": data.get("percent", 0),
        },
    )
    await ctx.refresh()


async def on_files_complete(ctx: Context):
    """Record completed uploads."""
    files = ctx.event_data.get("files", [])
    existing: list[dict[str, Any]] = ctx.state.get("completed_files", [])
    existing.extend(files)
    ctx.state.set("completed_files", existing)
    await ctx.refresh()


async def on_file_removed(ctx: Context):
    """Remove a file from the completed list by name."""
    removed_name = ctx.event_data.get("file", {}).get("name")
    completed: list[dict[str, Any]] = ctx.state.get("completed_files", [])
    ctx.state.set(
        "completed_files",
        [f for f in completed if f.get("name") != removed_name],
    )
    await ctx.refresh()


# ─── Section 3: Dynamic CSV download ─────────────────────────────────────────

SAMPLE_DATA = [
    {"Name": "Alice", "Department": "Engineering", "Salary": "95000"},
    {"Name": "Bob", "Department": "Design", "Salary": "82000"},
    {"Name": "Carol", "Department": "Product", "Salary": "110000"},
    {"Name": "Dave", "Department": "Engineering", "Salary": "105000"},
    {"Name": "Eve", "Department": "Marketing", "Salary": "78000"},
]


async def download_csv(ctx: Context):
    """Generate a CSV in memory and trigger a browser download."""
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=["Name", "Department", "Salary"])
    writer.writeheader()
    writer.writerows(SAMPLE_DATA)
    csv_bytes = buf.getvalue().encode("utf-8")

    filename = f"employees_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    url = await ctx.create_file_url(csv_bytes, filename, "text/csv")
    await ctx.trigger_download(url, filename)


# ─── Section 4: Inline image generation ──────────────────────────────────────


def _make_color_swatch_svg(color: str, label: str) -> bytes:
    """Create a tiny SVG colour swatch."""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="200" height="100">
  <rect width="200" height="100" fill="{color}"/>
  <text x="100" y="58" font-size="18" font-family="sans-serif"
        text-anchor="middle" fill="white" font-weight="bold">{label}</text>
</svg>"""
    return svg.encode("utf-8")


SWATCHES = [
    ("#2563eb", "Blue"),
    ("#16a34a", "Green"),
    ("#dc2626", "Red"),
    ("#9333ea", "Purple"),
]


async def show_swatch(ctx: Context, color: str, label: str):
    """Generate an SVG swatch and display it without a download prompt."""
    svg_bytes = _make_color_swatch_svg(color, label)
    # inline=True → Content-Disposition: inline, safe to use as <img src>
    url = await ctx.create_file_url(svg_bytes, f"{label}.svg", "image/svg+xml", inline=True)
    ctx.state.set("swatch_url", url)
    ctx.state.set("swatch_label", label)
    await ctx.refresh()


# ─── Page renderer ───────────────────────────────────────────────────────────


@ui.page("/")
def main_page(ctx: Context):
    image_url: str | None = ctx.state.get("uploaded_image_url")
    image_name: str | None = ctx.state.get("uploaded_image_name")
    image_error: str | None = ctx.state.get("image_error")
    selected_count: int = ctx.state.get("selected_count", 0)
    upload_progress: dict | None = ctx.state.get("upload_progress")
    completed_files: list[dict] = ctx.state.get("completed_files", [])
    swatch_url: str | None = ctx.state.get("swatch_url")
    swatch_label: str | None = ctx.state.get("swatch_label")

    return Container(
        class_name="max-w-4xl mx-auto p-8 space-y-8",
        children=[
            Heading("File Transfer Demo", level=1, class_name="text-3xl font-bold"),
            Paragraph(
                "This example demonstrates FileUploader, programmatic downloads, "
                "and inline file URLs.",
                class_name="text-muted-foreground",
            ),

            # ── Section 1: Image uploader ─────────────────────────────────
            Card(children=[
                CardHeader(children=[
                    CardTitle("1. Image Uploader (dropzone)"),
                    CardDescription("Upload an image – it will appear below after upload."),
                ]),
                CardContent(
                    class_name="space-y-4",
                    children=[
                        FileUploader(
                            label="Drop an image here",
                            description="PNG, JPG, GIF, WebP – max 5 MB",
                            variant="dropzone",
                            accept="image/*",
                            max_size=5 * 1024 * 1024,
                            on_upload_complete=ctx.callback(on_image_uploaded),
                            on_upload_error=ctx.callback(on_image_upload_error),
                        ),
                        *([Alert(image_error, variant="destructive")] if image_error else []),
                        *([
                            Column(
                                class_name="items-center gap-2",
                                children=[
                                    Text(f"Uploaded: {image_name}", class_name="text-sm font-medium"),
                                    Image(src=image_url, alt=image_name, class_name="max-h-64 rounded-md border"),
                                ],
                            )
                        ] if image_url else []),
                    ],
                ),
            ]),

            # ── Section 2: Multi-file uploader ────────────────────────────
            Card(children=[
                CardHeader(children=[
                    CardTitle("2. Multi-file Uploader (button variant)"),
                    CardDescription("Supports multiple files, progress reporting, and remove."),
                ]),
                CardContent(
                    class_name="space-y-4",
                    children=[
                        FileUploader(
                            label="Select files to upload",
                            variant="button",
                            multiple=True,
                            max_files=5,
                            max_size=10 * 1024 * 1024,
                            drag_drop=True,
                            on_select=ctx.callback(on_files_selected),
                            # Throttle progress events to max 1 per 300 ms
                            on_upload_progress=ctx.callback(on_files_progress, throttle=300),
                            on_upload_complete=ctx.callback(on_files_complete),
                            on_remove=ctx.callback(on_file_removed),
                        ),
                        *([Text(f"Files selected: {selected_count}", class_name="text-sm")] if selected_count else []),
                        *(
                            [Text(
                                f"Uploading {upload_progress['file']}: {upload_progress['percent']}%",
                                class_name="text-sm text-muted-foreground",
                            )]
                            if upload_progress else []
                        ),
                        *([
                            Column(
                                class_name="gap-1",
                                children=[
                                    Text("Uploaded files:", class_name="text-sm font-medium"),
                                    *[Badge(f["name"], variant="secondary") for f in completed_files],
                                ],
                            )
                        ] if completed_files else []),
                    ],
                ),
            ]),

            # ── Section 3: CSV download ───────────────────────────────────
            Card(children=[
                CardHeader(children=[
                    CardTitle("3. Dynamic CSV Download"),
                    CardDescription(
                        "Generate a CSV on the server and trigger a browser download "
                        "using ctx.trigger_download() — no FileDownloader component needed."
                    ),
                ]),
                CardContent(children=[
                    Button(
                        "Download Employee CSV",
                        on_click=ctx.callback(download_csv),
                        variant="outline",
                    ),
                ]),
            ]),

            # ── Section 4: Inline image generation ───────────────────────
            Card(children=[
                CardHeader(children=[
                    CardTitle("4. Inline File URL (no download prompt)"),
                    CardDescription(
                        "ctx.create_file_url(inline=True) returns a URL that can be "
                        "used as an <img src> without triggering a download."
                    ),
                ]),
                CardContent(
                    class_name="space-y-4",
                    children=[
                        Row(
                            class_name="gap-2 flex-wrap",
                            children=[
                                Button(
                                    label,
                                    on_click=ctx.callback(show_swatch, color=color, label=label),
                                    variant="outline",
                                )
                                for color, label in SWATCHES
                            ],
                        ),
                        *([
                            Column(
                                class_name="items-center gap-2",
                                children=[
                                    Text(f"Swatch: {swatch_label}", class_name="text-sm font-medium"),
                                    Image(
                                        src=swatch_url,
                                        alt=swatch_label,
                                        class_name="rounded border w-48 h-24",
                                    ),
                                ],
                            )
                        ] if swatch_url else []),
                    ],
                ),
            ]),
        ],
    )


# ─── ASGI app ─────────────────────────────────────────────────────────────────

fastapi_app = FastAPI()
fastapi_app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)
