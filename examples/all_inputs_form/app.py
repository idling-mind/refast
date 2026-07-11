"""Example showcasing all form inputs in Refast.

This includes basic inputs (Input, Textarea, Select, Checkbox, Switch, RadioGroup)
and the advanced inputs updated with name support (Slider, Toggle, ToggleGroup,
Calendar, DatePicker, InputOTP, FileUploader).
"""

import json
from fastapi import FastAPI
import uvicorn

from refast import Context, RefastApp
from refast.components import (
    Form,
    FormField,
    Input,
    Textarea,
    Switch,
    Toggle,
    ToggleGroup,
    ToggleGroupItem,
    Checkbox,
    RadioGroup,
    Radio,
    Select,
    Combobox,
    Slider,
    Calendar,
    DatePicker,
    InputOTP,
    FileUploader,
    Button,
    Card,
    CardHeader,
    CardTitle,
    CardDescription,
    CardContent,
    Column,
    Row,
    Container,
    Text,
    Alert,
    Heading, Label,
)

ui = RefastApp(title="Refast Form Controls Showcase")


async def handle_submit(ctx: Context, **kwargs):
    """Callback triggered on Form submit.

    Receives all named field values as keyword arguments.
    """
    # Store submission kwargs in state to show on screen
    ctx.state.set("submitted_data", kwargs)
    # Rerender the showcase container to show success message and the data
    await ctx.replace("showcase-container", render_showcase(ctx))


def render_showcase(ctx: Context):
    submitted_data = ctx.state.get("submitted_data", None)

    # Left-hand Column: The Form with all controls
    form_card = Card(
        class_name="border border-muted-foreground/10 shadow-lg",
        children=[
            CardHeader(
                children=[
                    CardTitle("Universal Form Controls"),
                    CardDescription(
                        "Fill out all the different inputs below. Submission triggers the on_submit callback."
                    ),
                ]
            ),
            CardContent(
                children=[
                    Form(
                        on_submit=ctx.callback(handle_submit),
                        class_name="space-y-6",
                        children=[
                            # Section 1: Standard Inputs
                            Column(
                                gap=4,
                                children=[
                                    Heading(
                                        "1. Text Inputs",
                                        level=3,
                                        class_name="text-sm font-semibold border-b pb-1 text-primary",
                                    ),
                                    FormField(
                                        label="Username",
                                        required=True,
                                        children=[
                                            Input(
                                                name="username",
                                                placeholder="enter your username",
                                                required=True,
                                            )
                                        ],
                                    ),
                                    FormField(
                                        label="Short Bio",
                                        children=[
                                            Textarea(
                                                name="bio",
                                                placeholder="Tell us a little bit about yourself...",
                                            )
                                        ],
                                    ),
                                ],
                            ),
                            # Section 2: Standard Select & Radios
                            Column(
                                gap=4,
                                children=[
                                    Heading(
                                        "2. Standard Choice Controls",
                                        level=3,
                                        class_name="text-sm font-semibold border-b pb-1 text-primary",
                                    ),
                                    FormField(
                                        label="Select Country",
                                        children=[
                                            Select(
                                                name="country",
                                                placeholder="Choose a country",
                                                options=[
                                                    {"value": "us", "label": "United States"},
                                                    {"value": "ca", "label": "Canada"},
                                                    {"value": "gb", "label": "United Kingdom"},
                                                    {"value": "de", "label": "Germany"},
                                                ],
                                            )
                                        ],
                                    ),
                                    FormField(
                                        label="Preferred Support Level",
                                        children=[
                                            RadioGroup(
                                                name="support_tier",
                                                value="standard",
                                                children=[
                                                    Radio(
                                                        value="basic", label="Basic (Email only)"
                                                    ),
                                                    Radio(
                                                        value="standard",
                                                        label="Standard (Business Hours)",
                                                    ),
                                                    Radio(
                                                        value="premium",
                                                        label="Premium (24/7 Priority Support)",
                                                    ),
                                                ],
                                            )
                                        ],
                                    ),
                                ],
                            ),
                            # Section 3: Switches, Checkbox & Combobox
                            Column(
                                gap=4,
                                children=[
                                    Heading(
                                        "3. Checkboxes & Multi-select",
                                        level=3,
                                        class_name="text-sm font-semibold border-b pb-1 text-primary",
                                    ),
                                    FormField(
                                        children=[
                                            Checkbox(
                                                name="subscribe_newsletter",
                                                label="Subscribe to newsletter?",
                                                value="newsletter_yes",
                                            )
                                        ]
                                    ),
                                    FormField(
                                        children=[
                                            Label("Enable high contrast mode"),
                                            Switch(
                                                name="enable_dark_mode",
                                            )
                                        ]
                                    ),
                                    FormField(
                                        label="Programming Languages of Interest (Combobox)",
                                        children=[
                                            Combobox(
                                                name="languages",
                                                multiselect=True,
                                                options=[
                                                    {"value": "python", "label": "Python"},
                                                    {"value": "typescript", "label": "TypeScript"},
                                                    {"value": "rust", "label": "Rust"},
                                                    {"value": "go", "label": "Go"},
                                                ],
                                            )
                                        ],
                                    ),
                                ],
                            ),
                            # Section 4: Advanced Controls with Name Support
                            Column(
                                gap=4,
                                children=[
                                    Heading(
                                        "4. Advanced Controls (New `name` Prop Support)",
                                        level=3,
                                        class_name="text-sm font-semibold border-b pb-1 text-primary",
                                    ),
                                    FormField(
                                        label="Experience Rating (Slider)",
                                        children=[
                                            Slider(
                                                name="rating",
                                                value=[75],
                                                min=0,
                                                max=100,
                                                step=5,
                                            )
                                        ],
                                    ),
                                    FormField(
                                        label="SaaS Agreement Status (Toggle)",
                                        children=[
                                            Toggle(
                                                name="saas_agreement",
                                                label="Accept Developer Agreement?",
                                                pressed=False,
                                                variant="outline",
                                            )
                                        ],
                                    ),
                                    FormField(
                                        label="Workstation Options (ToggleGroup)",
                                        children=[
                                            ToggleGroup(
                                                name="workstation_options",
                                                type="multiple",
                                                children=[
                                                    ToggleGroupItem(
                                                        value="monitor", label="Dual Monitors"
                                                    ),
                                                    ToggleGroupItem(
                                                        value="mouse", label="Ergonomic Mouse"
                                                    ),
                                                    ToggleGroupItem(
                                                        value="keyboard",
                                                        label="Mechanical Keyboard",
                                                    ),
                                                ],
                                            )
                                        ],
                                    ),
                                    FormField(
                                        label="Important Milestones (Calendar)",
                                        children=[
                                            Calendar(
                                                name="milestone_calendar",
                                                mode="multiple",
                                            )
                                        ],
                                    ),
                                    FormField(
                                        label="Preferred Release Date (DatePicker)",
                                        children=[
                                            DatePicker(
                                                name="release_date",
                                                mode="single",
                                                placeholder="Choose target date",
                                            )
                                        ],
                                    ),
                                    FormField(
                                        label="One-Time Verification Pin (InputOTP)",
                                        children=[
                                            InputOTP(
                                                name="otp_pin",
                                                max_length=6,
                                            )
                                        ],
                                    ),
                                    FormField(
                                        label="Profile Attachments (FileUploader)",
                                        children=[
                                            FileUploader(
                                                name="profile_attachments",
                                                multiple=True,
                                                max_files=3,
                                                upload_url="/api/upload",
                                            )
                                        ],
                                    ),
                                ],
                            ),
                            # Submit Button
                            Button(
                                "Submit All Form Data",
                                type="submit",
                                class_name="w-full bg-primary text-primary-foreground py-2 font-medium shadow-md hover:opacity-90",
                            ),
                        ],
                    )
                ]
            ),
        ],
    )

    # Right-hand Column: Displaying the Submitted Data
    submitted_card = Card(
        class_name="border border-muted-foreground/10 bg-slate-950/40 backdrop-blur-sm shadow-inner self-start",
        children=[
            CardHeader(
                children=[
                    CardTitle("Received Server Payload"),
                    CardDescription("Submitted form kwargs will show here in real-time."),
                ]
            ),
            CardContent(
                children=[
                    Column(
                        gap=4,
                        children=[
                            Alert(
                                variant="success",
                                title="Form Submitted!",
                                message="The server successfully intercepted the form submission.",
                            )
                            if submitted_data is not None
                            else Alert(
                                variant="info",
                                title="Awaiting Submission",
                                message="Fill in the fields on the left and click 'Submit All Form Data' to see the payload.",
                            ),
                            Text(
                                "Kwargs payload from on_submit callback:",
                                class_name="text-xs text-muted-foreground uppercase font-bold tracking-wider",
                            ),
                            Text(
                                json.dumps(submitted_data, indent=2)
                                if submitted_data is not None
                                else "{}",
                                class_name="p-4 bg-black/60 font-mono text-xs rounded border border-muted-foreground/20 overflow-auto max-h-[600px] text-green-400 whitespace-pre-wrap",
                            ),
                        ],
                    )
                ]
            ),
        ],
    )

    # Layout: Horizontal split on desktop, vertical stack on mobile
    return Row(
        id="showcase-container",
        class_name="grid grid-cols-1 md:grid-cols-2 gap-6 items-start mt-6",
        children=[
            form_card,
            submitted_card,
        ],
    )


@ui.page("/")
def home(ctx: Context):
    return Container(
        class_name="max-w-7xl mx-auto p-6 space-y-6",
        children=[
            Column(
                children=[
                    Heading(
                        "Refast Form Submission Showcase",
                        level=1,
                        class_name="text-3xl font-extrabold tracking-tight",
                    ),
                    Text(
                        "This example demonstrates how all controls (both standard and advanced) submit their values to a single on_submit server callback.",
                        class_name="text-muted-foreground text-sm",
                    ),
                ]
            ),
            render_showcase(ctx),
        ],
    )


# Create FastAPI application
app = FastAPI()
app.include_router(ui.router)


@app.post("/api/upload")
async def dummy_upload():
    """Dummy file upload endpoint to satisfy FileUploader uploads."""
    import uuid

    return {
        "id": f"file-{uuid.uuid4().hex[:8]}",
        "name": "uploaded_document.pdf",
        "size": 102456,
        "content_type": "application/pdf",
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
