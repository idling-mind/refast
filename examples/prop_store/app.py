"""Prop Store Example - Frontend-Only State for Forms.

This example demonstrates the prop_store feature which allows you to:
- Capture input values on the frontend without server roundtrips
- Access all stored values when any callback is triggered
- Build forms with minimal boilerplate

Compare this to the traditional form_validation example which requires
on_change callbacks for every input to sync state to the server.
"""

from fastapi import FastAPI

from refast import Context, RefastApp
from refast.components import (
    Alert,
    Badge,
    Button,
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
    Column,
    Container,
    Heading,
    Input,
    Label,
    Row,
    Separator,
    Text,
)

ui = RefastApp(title="Prop Store Example")


async def handle_submit(ctx: Context, fullname: str = "", email: str = "", message: str = ""):
    """Handle form submission using prop values passed as arguments.
    
    Note: Props requested via props=["fullname", "email", "message"] are 
    passed directly as keyword arguments - no need to use ctx.prop_store!
    """
    print(f"Form submitted: fullname={fullname}, email={email}, message={message}")
    
    # Validation
    errors = []
    if not fullname:
        errors.append("Name is required")
    if not email or "@" not in email:
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
        ctx.state.set("submitted_data", {
            "fullname": fullname,
            "email": email,
            "message": message,
        })
    
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
        children.extend([
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
                                ]
                            ),
                            Row(
                                class_name="gap-2 mt-2",
                                children=[
                                    Badge("Email:"),
                                    Text(submitted_data.get("email", "")),
                                ]
                            ),
                            Row(
                                class_name="gap-2 mt-2",
                                children=[
                                    Badge("Message:"),
                                    Text(submitted_data.get("message", "")),
                                ]
                            ),
                        ]
                    ),
                ]
            ),
        ])
    
    return Column(
        id="result-area",
        class_name="mt-4 gap-2",
        children=children if children else [Text("")],
    )


@ui.page("/")
def home(ctx: Context):
    """Render the contact form using prop_store for input capture."""
    return Container(
        class_name="mt-10 p-4",
        style={"maxWidth": "32rem", "marginLeft": "auto", "marginRight": "auto"},
        children=[
            Card(
                children=[
                    CardHeader(
                        children=[
                            CardTitle("Contact Form"),
                            CardDescription(
                                "Using prop_store for frontend-only state"
                            ),
                        ]
                    ),
                    CardContent(
                        children=[
                            # Explanation
                            Alert(
                                variant="default",
                                title="How it works",
                                message=(
                                    "Input values are stored on the frontend via store_as. "
                                    "No server roundtrips occur until you click Submit. "
                                    "Then all values are sent with the callback."
                                ),
                                class_name="mb-4",
                            ),
                            
                            # Name field - uses store_as to capture value
                            Column(
                                class_name="gap-2 mb-4",
                                children=[
                                    Input(
                                        id="name",
                                        label="Name",
                                        name="name",
                                        placeholder="Enter your name",
                                        # store_as="name" captures the input value
                                        # without a server roundtrip
                                        on_change=ctx.callback(store_as="fullname"),
                                    ),
                                ]
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
                                        on_change=ctx.callback(store_as="email"),
                                    ),
                                ]
                            ),
                            
                            # Message field
                            Column(
                                class_name="gap-2 mb-4",
                                children=[
                                    Input(
                                        id="message",
                                        label="Message",
                                        name="message",
                                        placeholder="Enter your message",
                                        on_change=ctx.callback(store_as="message"),
                                    ),
                                ]
                            ),
                            
                            Separator(class_name="my-4"),
                            
                            # Submit button - request specific props as kwargs
                            Button(
                                "Submit",
                                on_click=ctx.callback(
                                    handle_submit,
                                    props=["fullname", "email", "message"]
                                ),
                                class_name="w-full",
                            ),
                        ]
                    ),
                ]
            ),
            
            # Result area (updated after submission)
            render_result(ctx),
        ]
    )


# Create FastAPI app and include Refast router
app = FastAPI()
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
