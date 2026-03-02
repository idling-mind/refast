"""Form Validation Example.

This example demonstrates:
- Form handling with Input components
- State management for form fields
- Validation logic
- Error and Success feedback using Alert
"""

from fastapi import FastAPI

from refast import Context, RefastApp
from refast.components import (
    Alert,
    Button,
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
    Column,
    Container,
    Input,
)

ui = RefastApp(title="Form Validation Example")


async def update_field(ctx: Context, name: str, value: str):
    """Update form field in state."""
    form_data = ctx.state.get("form_data", {})
    form_data[name] = value
    ctx.state.set("form_data", form_data)


async def handle_submit(ctx: Context, **kwargs):
    """Validate and submit the form."""
    name = kwargs.get("name", "")
    email = kwargs.get("email", "")
    password = kwargs.get("password", "")
    confirm_password = kwargs.get("confirm_password", "")

    errors = []
    if not name:
        errors.append("Name is required")
    else:
        ctx.state.set("name", name)  # Save name to state for persistence
    if not email or "@" not in email:
        errors.append("Valid email is required")
    else:
        ctx.state.set("email", email)  # Save email to state for persistence
    if not password or len(password) < 6:
        errors.append("Password must be at least 6 characters")
    else:
        ctx.state.set("password", password)  # Save password to state for persistence
    if password != confirm_password:
        errors.append("Passwords do not match")
    else:
        ctx.state.set("confirm_password", confirm_password)  # Save confirm_password to state for persistence

    if errors:
        ctx.state.set("errors", errors)
        ctx.state.set("success", False)
    else:
        ctx.state.set("errors", [])
        ctx.state.set("success", True)

    await ctx.replace("form-container", render_form(ctx))


def render_form(ctx: Context):
    errors = ctx.state.get("errors", [])
    success = ctx.state.get("success", False)
    form_data = ctx.state.get("form_data", {})

    return Container(
        id="form-container",
        class_name="mt-10 p-4",
        style={"maxWidth": "28rem", "marginLeft": "auto", "marginRight": "auto"},
        children=[
            Card(
                id="registration-card",
                children=[
                    CardHeader(
                        id="card-header",
                        children=[
                            CardTitle("Registration"),
                            CardDescription("Create a new account"),
                        ]
                    ),
                    CardContent(
                        id="card-content",
                        children=[
                            Column(
                                id="form-column",
                                gap=4,
                                children=[
                                    # Error Alerts
                                    *[
                                        Alert(variant="destructive", title="Error", message=err)
                                        for err in errors
                                    ],
                                    # Success Alert
                                    Alert(
                                        variant="success",
                                        title="Success",
                                        message="Account created successfully!",
                                    )
                                    if success
                                    else None,
                                    # Form Fields
                                    Input(
                                        id="input-name",
                                        name="name",
                                        label="Full Name",
                                        placeholder="John Doe",
                                        value=form_data.get("name", ""),
                                        on_change=ctx.save_prop("name")
                                    ),
                                    Input(
                                        id="input-email",
                                        name="email",
                                        label="Email",
                                        type="email",
                                        placeholder="john@example.com",
                                        value=form_data.get("email", ""),
                                        on_change=ctx.save_prop("email"),
                                    ),
                                    Input(
                                        id="input-password",
                                        name="password",
                                        label="Password",
                                        type="password",
                                        value=form_data.get("password", ""),
                                        on_change=ctx.save_prop("password"),
                                    ),
                                    Input(
                                        id="input-confirm-password",
                                        name="confirm_password",
                                        label="Confirm Password",
                                        type="password",
                                        value=form_data.get("confirm_password", ""),
                                        on_change=ctx.save_prop("confirm_password"),
                                    ),
                                    # Submit Button
                                    Button(
                                        "Register",
                                        on_click=ctx.callback(
                                            handle_submit,
                                            props=["name", "email", "password", "confirm_password"],
                                        ),
                                        class_name="w-full",
                                    ),
                                ],
                            )
                        ]
                    ),
                ]
            )
        ],
    )


@ui.page("/")
def home(ctx: Context):
    return render_form(ctx)


# Create FastAPI app
app = FastAPI()
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
