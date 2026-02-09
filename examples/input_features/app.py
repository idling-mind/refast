"""
Example showcasing the improved Input component features:
- Label with required asterisk
- Description text
- Error states
- Additional keyboard events
"""

from fastapi import FastAPI

from refast import Context, RefastApp
from refast.components import (
    Button,
    Card,
    CardContent,
    CardHeader,
    CardTitle,
    Column,
    Container,
    Heading,
    Input,
)

ui = RefastApp(title="Input Component Features")


async def set_state(ctx: Context, key: str):
    """Set state value on input change."""
    value = ctx.event_data.get("value", "")
    ctx.state.set(key, value)


async def validate_email(ctx: Context):
    """Validate email on change."""
    value = ctx.event_data.get("value", "")
    if "@" in value and "." in value:
        await ctx.update_props("email", {"error": ""})
        ctx.state.set("email", value)
    else:
        await ctx.update_props("email", {"error": "Please enter a valid email address"})


async def validate_password(ctx: Context):
    """Validate password on change."""
    value = ctx.event_data.get("value", "")
    if len(value) >= 8:
        await ctx.update_props("password", {"error": ""})
        ctx.state.set("password", value)
    else:
        await ctx.update_props("password", {"error": "Password must be at least 8 characters"})


async def handle_keydown(ctx: Context):
    """Handle keydown event."""
    key = ctx.event_data.get("key", "")
    if key == "Enter":
        ctx.state.set("message", "Enter key pressed!")


async def handle_submit(ctx: Context):
    """Handle form submission."""
    email = ctx.state.get("email", "")
    password = ctx.state.get("password", "")
    username = ctx.state.get("username", "")

    if email and password and username:
        await ctx.show_toast(
            "Success", variant="success", description="Account created successfully!"
        )
    else:
        await ctx.show_toast(
            "Error", variant="error", description="Please fill in all required fields."
        )


@ui.page("/")
def home(ctx: Context):
    """Input component feature showcase."""

    return Container(
        class_name="max-w-4xl mx-auto p-4",
        children=[
            Heading("Input Component Features", level=1),
            Card(
                class_name="max-w-4xl mx-auto mt-8",
                children=[
                    CardHeader(children=[CardTitle("Registration Form")]),
                    CardContent(
                        children=[
                            Column(
                                class_name="space-y-6",
                                children=[
                                    # Input with label and required asterisk
                                    Input(
                                        name="username",
                                        label="Username",
                                        description="Choose a unique username",
                                        placeholder="johndoe",
                                        required=True,
                                        value=ctx.state.get("username", ""),
                                        on_change=ctx.callback(set_state, key="username"),
                                        debounce=300,
                                    ),
                                    # Input with validation and error state
                                    Input(
                                        id="email",
                                        name="email",
                                        type="email",
                                        label="Email Address",
                                        description="We'll never share your email",
                                        placeholder="you@example.com",
                                        required=True,
                                        value=ctx.state.get("email", ""),
                                        on_change=ctx.callback(validate_email),
                                        debounce=300,
                                    ),
                                    # Input with keyboard events
                                    Input(
                                        id="password",
                                        name="password",
                                        type="password",
                                        label="Password",
                                        description="Must be at least 8 characters",
                                        placeholder="••••••••",
                                        required=True,
                                        value=ctx.state.get("password", ""),
                                        on_change=ctx.callback(validate_password),
                                        debounce=300,
                                    ),
                                    # Optional input without required
                                    Input(
                                        id="phone",
                                        name="phone",
                                        type="tel",
                                        label="Phone Number",
                                        description="Optional - for account recovery",
                                        placeholder="+1 (555) 000-0000",
                                        value=ctx.state.get("phone", ""),
                                        on_change=ctx.callback(set_state, key="phone"),
                                        debounce=300,
                                    ),
                                    # Submit button
                                    Button(
                                        id="submit-btn",
                                        label="Create Account",
                                        variant="default",
                                        class_name="w-full",
                                        on_click=ctx.callback(handle_submit),
                                    ),
                                ],
                            )
                        ]
                    ),
                ],
            ),
        ],
    )


app = FastAPI()
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
