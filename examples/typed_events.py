import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field, ValidationError

from refast import Context, RefastApp
from refast.components import (
    Button,
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
    Center,
    Column,
    Heading,
    Input,
    Row,
    Text,
)
from refast.events.types import Event

# Define a Pydantic model for structured event validation
class SearchQueryPayload(BaseModel):
    query: str = Field(..., min_length=2, description="The search query text")
    limit: int = Field(5, ge=1, le=50, description="Number of results to return")


ui = RefastApp(title="Typed Events & Parameters", debug=True)


# Custom error handler for the custom event
async def event_error_handler(ctx: Context, error: Exception, event: Event):
    ctx.state["query_result"] = f"Custom Event Validation Failed: {error}"
    await ctx.show_toast(
        message="Event Validation Error (Handled)",
        description="Check the form values. Query must be at least 2 chars.",
        variant="warning"
    )
    await ctx.refresh()


# Custom error handler for the callback
async def callback_error_handler(ctx: Context, error: Exception, **kwargs):
    if not isinstance(error, ValidationError):
        await ctx.show_toast("Some error", description=str(error))
        return
    ctx.state["query_result"] = f"Callback Validation Failed: {error}"
    await ctx.show_toast(
        message="Callback Validation Error (Handled)",
        description="Check the form values. Query must be at least 2 chars.",
        variant="warning"
    )
    await ctx.refresh()


# ---------------------------------------------------------------------------
# 1. Typed Event Handler Example
# ---------------------------------------------------------------------------
# Registers custom error handling via the on_error parameter.
# If validation fails, `event_error_handler` is invoked instead of showing the default toast.
@ui.on("search:query_event", on_error=event_error_handler)
async def handle_search_event(ctx: Context, event: Event[SearchQueryPayload]):
    query = event.data.query
    limit = event.data.limit
    
    ctx.state["query_result"] = f"Event received! Query: '{query}', Limit: {limit}"
    await ctx.show_toast(
        message="Typed Event Validated!",
        description=f"Query: {query} (Limit: {limit})",
        variant="default"
    )
    await ctx.refresh()


# ---------------------------------------------------------------------------
# 2. Typed Callback Parameter Example
# ---------------------------------------------------------------------------
async def run_search_callback(ctx: Context, payload: SearchQueryPayload):
    query = payload.query
    limit = payload.limit
    
    ctx.state["query_result"] = f"Callback invoked! Query: '{query}', Limit: {limit}"
    await ctx.show_toast(
        message="Callback Validated!",
        description=f"Query: {query} (Limit: {limit})",
        variant="success"
    )
    await ctx.refresh()


# ---------------------------------------------------------------------------
# Page Layout
# ---------------------------------------------------------------------------
@ui.page("/")
def main_page(ctx: Context):
    query_result = ctx.state.get("query_result", "No action taken yet. Try entering a 1-character query to trigger validation errors.")
    
    return Center(
        Column(
            [
                Card(
                    [
                        CardHeader(
                            children=[
                                CardTitle("Typed Events & Callback Validation"),
                                CardDescription(
                                    "This example demonstrates Refast's automatic parameter validation using Pydantic models."
                                ),
                            ]
                        ),
                        CardContent(
                            Column(
                                [
                                    Heading("Search Parameters", level=3, class_name="mb-2"),
                                    Row(
                                        [
                                            Input(
                                                placeholder="Query (min 2 chars)",
                                                on_change=ctx.save_prop("query"),
                                                class_name="w-64"
                                            ),
                                            Input(
                                                placeholder="Limit (default 5, 1-50)",
                                                on_change=ctx.save_prop("limit"),
                                                class_name="w-32"
                                            ),
                                        ],
                                        gap=2
                                    ),
                                    Text(
                                        f"Status: {query_result}",
                                        class_name="mt-4 p-3 bg-muted rounded-md text-sm border"
                                    ),
                                ],
                                class_name="space-y-4"
                            )
                        ),
                        CardFooter(
                            Row(
                                [
                                    # 1. Triggering standard callback with registered custom error handler
                                    Button(
                                        "Trigger Callback",
                                        on_click=ctx.callback(
                                            run_search_callback, 
                                            props=["query", "limit"],
                                            on_error=callback_error_handler
                                        ),
                                        variant="default"
                                    ),
                                    # 2. Emitting a custom event directly from the frontend
                                    Button(
                                        "Emit Custom Event",
                                        on_click=ctx.js(
                                            "refast.emit('search:query_event', { query: refast.getProp('query'), limit: parseInt(refast.getProp('limit')) || 5 })"
                                        ),
                                        variant="secondary"
                                    ),
                                ],
                                gap=2
                            )
                        ),
                    ],
                    style={"width": "500px"}
                )
            ]
        ),
        class_name="h-screen bg-slate-50"
    )


app = FastAPI()
app.include_router(ui.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
