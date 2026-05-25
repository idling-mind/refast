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
    Score values are refreshed every 5 seconds; only the Progress bar
    props are patched via ctx.update_props (no full table re-render).

Run with:
    uvicorn examples.rich_table.app:app --reload
"""

import asyncio
import random
from contextlib import asynccontextmanager

from fastapi import FastAPI

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
        "keywords": "female",
    },
    {
        "id": 2,
        "name": "Bob Torres",
        "email": "bob@example.com",
        "role": "Editor",
        "status": "inactive",
        "score": 45,
        "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Bob",
        "keywords": "male",
    },
    {
        "id": 3,
        "name": "Carol Kim",
        "email": "carol@example.com",
        "role": "Viewer",
        "status": "pending",
        "score": 68,
        "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Carol",
        "keywords": "female",
    },
    {
        "id": 4,
        "name": "Dan Osei",
        "email": "dan@example.com",
        "role": "Editor",
        "status": "active",
        "score": 81,
        "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Dan",
        "keywords": "male",
    },
    {
        "id": 5,
        "name": "Eve Müller",
        "email": "eve@example.com",
        "role": "Admin",
        "status": "active",
        "score": 99,
        "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Eve",
        "keywords": "female",
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


def score_progress(score: int, user_id: int) -> Progress:
    return Progress(
        id=f"score-progress-{user_id}",
        value=score,
        max=100,
        show_value=True,
        foreground_color=(
            "#16a34a" if score >= 80 else "#d97706" if score >= 50 else "destructive"
        ),
        class_name="min-w-28",
    )


def _score_fg(score: int) -> str:
    return "#16a34a" if score >= 80 else "#d97706" if score >= 50 else "destructive"


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
# Background task — update scores every 5 seconds
# ---------------------------------------------------------------------------


async def _tick_scores() -> None:
    while True:
        await asyncio.sleep(5)
        print("Tick: updating scores...")
        for ctx in ui.active_contexts:
            scores: dict[int, int] = ctx.store.local.get(
                "scores", {u["id"]: u["score"] for u in USERS}
            )
            # Random walk: ±1–10 points, clamped to [1, 100]
            new_scores = {
                uid: max(1, min(100, s + random.randint(-10, 10)))
                for uid, s in scores.items()
            }
            ctx.store.local["scores"] = new_scores
            # Update only the individual Progress components — no table re-render
            for uid, score in new_scores.items():
                print(f"Updating user {uid} score to {score}")
                await ctx.update_props(
                    f"score-progress-{uid}",
                    {"value": score, "foreground_color": _score_fg(score)},
                )


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
    # Section B — DataTable with Component instances as cell values.
    # Each Progress has a stable id; the background task uses update_props
    # to patch only value+foreground_color — no table re-render needed.
    # ------------------------------------------------------------------

    scores: dict[int, int] = ctx.store.local.get(
        "scores", {u["id"]: u["score"] for u in USERS}
    )
    datatable_data = [
        {
            "name": user["name"],
            "avatar": Image(
                src=user["avatar"],
                alt=user["name"],
                width=36,
                height=36,
                class_name="rounded-full",
                object_fit="cover",
            ),
            "status": status_badge(user["status"]),
            "score": score_progress(scores.get(user["id"], user["score"]), user["id"]),
            "role": user["role"],
            "keywords": user["keywords"],
        }
        for user in USERS
    ]
    rich_datatable = DataTable(
        id="rich-datatable",
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
                                "Each Progress bar has a stable id. The background task calls "
                                "ctx.update_props to patch only value+color every 5 s — "
                                "no full table re-render. Click a row to see event_data.",
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
@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(_tick_scores())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


app = FastAPI(lifespan=lifespan)
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
