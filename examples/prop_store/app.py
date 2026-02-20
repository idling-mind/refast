"""Prop Store Example - Frontend-Only State for Forms.

This example demonstrates the prop store feature which allows you to:
- Capture input values on the frontend without server roundtrips (ctx.store_prop)
- Request stored values as keyword arguments in callbacks (props=[...])
- Compose multiple actions on a single event with ctx.chain
- Build forms with minimal boilerplate

Compare this to the traditional form_validation example which requires
on_change callbacks for every input to sync state to the server.
"""

import asyncio

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
    Input,
    Row,
    Separator,
    Text,
    Textarea,
)

ui = RefastApp(title="Prop Store Example")


async def show_typing(ctx: Context, message: str = ""):
    """Show typing indicator when user types in the message field."""
    message = ctx.state.get("message", "")  # Get the latest message value from state
    event_message = ctx.event_data.get("value", "")  # Get the current event message value
    print(f"show_typing called with message='{message}', event_message='{event_message}'")
    print("Message value has changed, showing typing indicator...")
    await ctx.update_text("result-area", "Typing...")
    ctx.state.set("message", event_message)  # Update state with the latest message value
    await asyncio.sleep(3)  # Simulate typing delay
    await ctx.update_text("result-area", "")  # Clear typing indicator after delay
    print("Typing indicator cleared.")


async def handle_submit(
    ctx: Context, input_name: str = "", input_email: str = "", message: str = ""
):
    """Handle form submission using prop values passed as arguments.

    Note: Props requested via props=["input_.*", "message"] are
    passed directly as keyword arguments to this function.
    """
    print(f"Form submitted: fullname={input_name}, email={input_email}, message={message}")

    # Validation
    errors = []
    if not input_name:
        errors.append("Name is required")
    if not input_email or "@" not in input_email:
        errors.append("Valid email is required")
    if not message:
        errors.append("Message is required")
    print(f"Validation errors: {errors}")

    if errors:
        ctx.state.set("errors", errors)
        ctx.state.set("success", False)
        ctx.state.set("submitted_data", None)
    else:
        ctx.state.set("errors", [])
        ctx.state.set("success", True)
        ctx.state.set(
            "submitted_data",
            {
                "fullname": input_name,
                "email": input_email,
                "message": message,
            },
        )

    await ctx.replace("result-area", render_result(ctx))


def render_result(ctx: Context):
    """Render the submission result."""
    errors = ctx.state.get("errors", [])
    success = ctx.state.get("success", False)
    submitted_data = ctx.state.get("submitted_data")

    children = []

    if errors:
        children.append(
            Alert(
                variant="destructive",
                title="Validation Errors",
                message=", ".join(errors),
            )
        )
    elif success and submitted_data:
        children.extend(
            [
                Alert(
                    variant="default",
                    title="Success!",
                    description="Form submitted successfully",
                ),
                Card(
                    class_name="mt-4",
                    children=[
                        CardHeader(
                            children=[
                                CardTitle("Submitted Data"),
                            ]
                        ),
                        CardContent(
                            children=[
                                Row(
                                    class_name="gap-2",
                                    children=[
                                        Badge("Name:"),
                                        Text(submitted_data.get("fullname", "")),
                                    ],
                                ),
                                Row(
                                    class_name="gap-2 mt-2",
                                    children=[
                                        Badge("Email:"),
                                        Text(submitted_data.get("email", "")),
                                    ],
                                ),
                                Row(
                                    class_name="gap-2 mt-2",
                                    children=[
                                        Badge("Message:"),
                                        Text(submitted_data.get("message", "")),
                                    ],
                                ),
                            ]
                        ),
                    ],
                ),
            ]
        )

    return Column(
        id="result-area",
        class_name="mt-4 gap-2",
        children=children if children else [Text("")],
    )


@ui.page("/")
def home(ctx: Context):
    """Render the contact form using store_prop for input capture."""
    return Container(
        class_name="mt-10 p-4",
        style={"maxWidth": "32rem", "marginLeft": "auto", "marginRight": "auto"},
        children=[
            Card(
                children=[
                    CardHeader(
                        children=[
                            CardTitle("Contact Form"),
                            CardDescription("Using ctx.store_prop for frontend-only state"),
                        ]
                    ),
                    CardContent(
                        children=[
                            # Explanation
                            Alert(
                                variant="default",
                                title="How it works",
                                message=(
                                    "Input values are stored on the frontend via ctx.store_prop. "
                                    "No server roundtrips occur until you click Submit. "
                                    "Then all values are sent with the callback."
                                ),
                                class_name="mb-4",
                            ),
                            # Name field - uses store_prop to capture value
                            Column(
                                class_name="gap-2 mb-4",
                                children=[
                                    Input(
                                        id="name",
                                        label="Name",
                                        name="name",
                                        placeholder="Enter your name",
                                        # ctx.store_prop("input_name") captures the input
                                        # value without a server roundtrip
                                        on_change=ctx.store_prop("input_name"),
                                    ),
                                ],
                            ),
                            # Email field
                            Column(
                                class_name="gap-2 mb-4",
                                children=[
                                    Input(
                                        id="email",
                                        label="Email",
                                        name="email",
                                        type="email",
                                        placeholder="Enter your email",
                                        on_change=ctx.store_prop("input_email"),
                                        debounce=500,
                                    ),
                                ],
                            ),
                            # Message field
                            Column(
                                class_name="gap-2 mb-4",
                                children=[
                                    Textarea(
                                        id="message",
                                        label="Message",
                                        name="message",
                                        placeholder="Enter your message",
                                        on_change=ctx.chain(
                                            [
                                                ctx.store_prop("message"),
                                                ctx.callback(show_typing, debounce=300),
                                                ctx.js(
                                                    "console.log('Message changed:', event.value)",
                                                    debounce=300,
                                                ),
                                            ]
                                        ),
                                    ),
                                ],
                            ),
                            Separator(class_name="my-4"),
                            # Submit button - request specific props as kwargs
                            Button(
                                "Submit",
                                on_click=ctx.callback(handle_submit, props=["input_.*", "message"]),
                                class_name="w-full",
                            ),
                        ]
                    ),
                ]
            ),
            # Result area (updated after submission)
            render_result(ctx),
        ],
    )


# Create FastAPI app and include Refast router
app = FastAPI()
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
