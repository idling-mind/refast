"""
Rich Table Example — components inside table cells.

Demonstrates two approaches:

  Section A — Table primitives
    Use TableCell(children=[...]) to embed any component directly.
    Each row shows: Avatar+name, Status Badge, Progress bar,
    Action Button, and a "linked text" ghost Button.

  Section B — DataTable with component cell values
    Put Component instances as dict values in the `data` list.
    DataTable serialises them automatically; the frontend renders
    them via ComponentRenderer just like any other component.

Run with:
    uvicorn examples.rich_table.app:app --reload
"""

from refast import Context, RefastApp
from refast.components import (
    Avatar,
    Badge,
    Button,
    Card,
    CardContent,
    CardHeader,
    Column,
    Container,
    DataTable,
    Heading,
    Image,
    Progress,
    Row,
    Separator,
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
    Text,
)

ui = RefastApp(title="Rich Table — Component Cells")

# ---------------------------------------------------------------------------
# Sample dataset
# ---------------------------------------------------------------------------

USERS = [
    {
        "id": 1,
        "name": "Alice Chen",
        "email": "alice@example.com",
        "role": "Admin",
        "status": "active",
        "score": 92,
        "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Alice",
    },
    {
        "id": 2,
        "name": "Bob Torres",
        "email": "bob@example.com",
        "role": "Editor",
        "status": "inactive",
        "score": 45,
        "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Bob",
    },
    {
        "id": 3,
        "name": "Carol Kim",
        "email": "carol@example.com",
        "role": "Viewer",
        "status": "pending",
        "score": 68,
        "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Carol",
    },
    {
        "id": 4,
        "name": "Dan Osei",
        "email": "dan@example.com",
        "role": "Editor",
        "status": "active",
        "score": 81,
        "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Dan",
    },
    {
        "id": 5,
        "name": "Eve Müller",
        "email": "eve@example.com",
        "role": "Admin",
        "status": "active",
        "score": 99,
        "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Eve",
    },
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

STATUS_VARIANT = {
    "active": "success",
    "inactive": "secondary",
    "pending": "warning",
}


def status_badge(status: str) -> Badge:
    return Badge(
        children=[status.capitalize()],
        variant=STATUS_VARIANT.get(status, "default"),
    )


# ---------------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------------


async def on_action(ctx: Context, name: str) -> None:
    await ctx.show_toast(f"Action triggered for {name}!")


async def on_link_click(ctx: Context) -> None:
    name = ctx.bound_args.get("name", "unknown")
    email = ctx.bound_args.get("email", "")
    await ctx.show_toast(f"Opened profile: {name} <{email}>")


async def on_row_click(ctx: Context) -> None:
    row = ctx.event_data
    await ctx.show_toast(f"Row clicked: {row.get('name', row)}")


# ---------------------------------------------------------------------------
# Page
# ---------------------------------------------------------------------------


@ui.page("/")
def home(ctx: Context):
    # ------------------------------------------------------------------
    # Section A — Table primitives with component children
    # ------------------------------------------------------------------
    primitive_rows = []
    for user in USERS:
        avatar_cell = TableCell(
            children=[
                Row(
                    gap=3,
                    align="center",
                    children=[
                        # Avatar with image src (falls back to initial)
                        Avatar(
                            src=user["avatar"],
                            fallback=user["name"][0],
                            size="sm",
                        ),
                        Column(
                            gap=0,
                            children=[
                                Text(user["name"], class_name="font-medium text-sm"),
                                Text(
                                    user["email"],
                                    class_name="text-xs text-muted-foreground",
                                ),
                            ],
                        ),
                    ],
                )
            ]
        )

        status_cell = TableCell(children=[status_badge(user["status"])])

        progress_cell = TableCell(
            children=[
                Container(
                    class_name="min-w-32",
                    children=[
                        Progress(
                            value=user["score"],
                            max=100,
                            show_value=True,
                            foreground_color=(
                                "#16a34a"
                                if user["score"] >= 80
                                else "#d97706"
                                if user["score"] >= 50
                                else "destructive"
                            ),
                        )
                    ],
                )
            ]
        )

        action_cell = TableCell(
            children=[
                Button(
                    label="Edit",
                    variant="outline",
                    size="sm",
                    on_click=ctx.callback(on_action, name=user["name"]),
                )
            ]
        )

        # Ghost button as "linked text"
        link_cell = TableCell(
            children=[
                Button(
                    label=user["name"],
                    variant="ghost",
                    size="sm",
                    class_name="p-0 h-auto font-normal underline-offset-4 hover:underline",
                    on_click=ctx.callback(
                        on_link_click, name=user["name"], email=user["email"]
                    ),
                )
            ]
        )

        primitive_rows.append(
            TableRow(
                children=[
                    avatar_cell,
                    status_cell,
                    progress_cell,
                    action_cell,
                    link_cell,
                ]
            )
        )

    primitive_table = Table(
        children=[
            TableHeader(
                children=[
                    TableRow(
                        children=[
                            TableHead(children=["User"]),
                            TableHead(children=["Status"]),
                            TableHead(children=["Score"]),
                            TableHead(children=["Action"]),
                            TableHead(children=["Profile Link"]),
                        ]
                    )
                ]
            ),
            TableBody(children=primitive_rows),
        ]
    )

    # ------------------------------------------------------------------
    # Section B — DataTable with Component instances as cell values
    # Each row dict contains a mix of plain values and Component objects.
    # DataTable serialises Component values automatically.
    # ------------------------------------------------------------------

    datatable_data = []
    for user in USERS:
        datatable_data.append(
            {
                # Plain string — rendered as text (unchanged behaviour)
                "name": user["name"],
                # Image component — rendered as a small avatar thumbnail
                "avatar": Image(
                    src=user["avatar"],
                    alt=user["name"],
                    width=36,
                    height=36,
                    class_name="rounded-full",
                    object_fit="cover",
                ),
                # Badge component — rendered with colour variant
                "status": status_badge(user["status"]),
                # Progress component — numeric bar
                "score": Progress(
                    value=user["score"],
                    max=100,
                    show_value=True,
                    foreground_color=(
                        "#16a34a"
                        if user["score"] >= 80
                        else "#d97706"
                        if user["score"] >= 50
                        else "destructive"
                    ),
                    class_name="min-w-28",
                ),
                # Plain string
                "role": user["role"],
            }
        )

    rich_datatable = DataTable(
        columns=[
            {"key": "avatar", "header": "Photo", "width": "60px"},
            {"key": "name", "header": "Name", "sortable": True},
            {"key": "status", "header": "Status", "sortable": True},
            {"key": "score", "header": "Score", "width": "160px"},
            {"key": "role", "header": "Role", "sortable": True},
        ],
        data=datatable_data,
        sortable=True,
        filterable=True,
        paginated=False,
        on_row_click=ctx.callback(on_row_click),
    )

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------
    return Container(
        class_name="max-w-5xl mx-auto p-6 space-y-10",
        children=[
            Heading("Rich Table — Components in Cells", level=1),
            Text(
                "Components can be placed inside table cells in two ways: "
                "as children of TableCell (full control) or as values in a "
                "DataTable data dict (automatic serialisation).",
                class_name="text-muted-foreground",
            ),
            Separator(),
            # --- Section A ---
            Card(
                children=[
                    CardHeader(
                        children=[
                            Heading("Section A — Table primitives", level=2),
                            Text(
                                "Each TableCell holds a Component directly. "
                                "Avatar+name / Badge / Progress / Button / ghost link.",
                                class_name="text-sm text-muted-foreground",
                            ),
                        ]
                    ),
                    CardContent(children=[primitive_table]),
                ]
            ),
            # --- Section B ---
            Card(
                children=[
                    CardHeader(
                        children=[
                            Heading("Section B — DataTable with component cells", level=2),
                            Text(
                                "Component instances placed as values in the row dict are "
                                "serialised automatically. Plain string/number values continue "
                                "to render as text. Click a row to see event_data.",
                                class_name="text-sm text-muted-foreground",
                            ),
                        ]
                    ),
                    CardContent(children=[rich_datatable]),
                ]
            ),
        ],
    )


# FastAPI app entry-point
from fastapi import FastAPI

app = FastAPI()
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
