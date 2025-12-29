"""Settings Panel Example - Multi-section settings with various input types.

This example demonstrates:
- Sidebar navigation with menu
- Form sections with different input types
- Switch, Select, Input, Textarea components
- Accordion for collapsible sections
- Toast notifications for save actions
"""

from fastapi import FastAPI

from refast import Context, RefastApp
from refast.components import (
    Avatar,
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
    Label,
    Row,
    Select,
    Separator,
    Switch,
    Text,
    Textarea,
)

# Create the Refast app
ui = RefastApp(title="Settings Panel")


# Callback handlers
async def save_profile(ctx: Context):
    """Save profile settings."""
    await ctx.show_toast("Profile saved successfully!", variant="success")


async def save_notifications(ctx: Context):
    """Save notification settings."""
    await ctx.show_toast("Notification preferences updated!", variant="success")


async def save_appearance(ctx: Context):
    """Save appearance settings."""
    await ctx.show_toast("Appearance settings saved!", variant="success")


async def toggle_setting(ctx: Context):
    """Toggle a boolean setting."""
    key = ctx.event_data.get("key")
    current = ctx.state.get(key, False)
    ctx.state.set(key, not current)


async def update_input(ctx: Context):
    """Update an input value."""
    key = ctx.event_data.get("key")
    value = ctx.event_data.get("value", "")
    ctx.state.set(key, value)


async def change_section(ctx: Context):
    """Change active section."""
    section = ctx.event_data.get("section")
    ctx.state.set("active_section", section)
    await ctx.refresh()


# Main page
@ui.page("/")
def home(ctx: Context):
    """Settings page."""
    active_section = ctx.state.get("active_section", "profile")

    # Default settings state
    email_notifications = ctx.state.get("email_notifications", True)
    push_notifications = ctx.state.get("push_notifications", False)
    marketing_emails = ctx.state.get("marketing_emails", False)
    weekly_digest = ctx.state.get("weekly_digest", True)
    theme = ctx.state.get("theme", "system")
    language = ctx.state.get("language", "en")

    # Menu items
    menu_items = [
        {"id": "profile", "label": "Profile", "icon": "user"},
        {"id": "notifications", "label": "Notifications", "icon": "bell"},
        {"id": "appearance", "label": "Appearance", "icon": "palette"},
        {"id": "security", "label": "Security", "icon": "shield"},
        {"id": "billing", "label": "Billing", "icon": "credit-card"},
    ]

    # Build content based on active section
    content = None

    if active_section == "profile":
        content = Card(
            children=[
                CardHeader(
                    children=[
                        CardTitle("Profile"),
                        CardDescription("Manage your public profile information"),
                    ]
                ),
                CardContent(
                    children=[
                        Column(
                            gap=6,
                            children=[
                                # Avatar section
                                Row(
                                    gap=4,
                                    align="center",
                                    children=[
                                        Avatar(
                                            src="https://github.com/shadcn.png",
                                            alt="User avatar",
                                            size="lg",
                                        ),
                                        Column(
                                            gap=2,
                                            children=[
                                                Button(
                                                    label="Change Avatar",
                                                    variant="outline",
                                                    size="sm",
                                                ),
                                                Text(
                                                    "JPG, GIF or PNG. Max size 2MB.",
                                                    class_name="text-xs text-muted-foreground",
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                Separator(),
                                # Name fields
                                Row(
                                    gap=4,
                                    children=[
                                        Column(
                                            gap=2,
                                            class_name="flex-1",
                                            children=[
                                                Label("First Name"),
                                                Input(
                                                    name="first_name",
                                                    placeholder="John",
                                                    value=ctx.state.get("first_name", ""),
                                                ),
                                            ],
                                        ),
                                        Column(
                                            gap=2,
                                            class_name="flex-1",
                                            children=[
                                                Label("Last Name"),
                                                Input(
                                                    name="last_name",
                                                    placeholder="Doe",
                                                    value=ctx.state.get("last_name", ""),
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                # Email
                                Column(
                                    gap=2,
                                    children=[
                                        Label("Email"),
                                        Input(
                                            name="email",
                                            type="email",
                                            placeholder="john@example.com",
                                            value=ctx.state.get("email", ""),
                                        ),
                                    ],
                                ),
                                # Username
                                Column(
                                    gap=2,
                                    children=[
                                        Label("Username"),
                                        Row(
                                            gap=0,
                                            children=[
                                                Container(
                                                    class_name="bg-muted px-3 py-2 rounded-l-md border border-r-0",
                                                    children=[
                                                        Text(
                                                            "@", class_name="text-muted-foreground"
                                                        )
                                                    ],
                                                ),
                                                Input(
                                                    name="username",
                                                    placeholder="johndoe",
                                                    value=ctx.state.get("username", ""),
                                                    class_name="rounded-l-none",
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                # Bio
                                Column(
                                    gap=2,
                                    children=[
                                        Label("Bio"),
                                        Textarea(
                                            name="bio",
                                            placeholder="Tell us a little about yourself",
                                            rows=4,
                                            value=ctx.state.get("bio", ""),
                                        ),
                                        Text(
                                            "Brief description for your profile. URLs are hyperlinked.",
                                            class_name="text-xs text-muted-foreground",
                                        ),
                                    ],
                                ),
                                # Save button
                                Row(
                                    justify="end",
                                    children=[
                                        Button(
                                            label="Save Changes",
                                            on_click=ctx.callback(save_profile),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

    elif active_section == "notifications":
        content = Card(
            children=[
                CardHeader(
                    children=[
                        CardTitle("Notifications"),
                        CardDescription("Configure how you receive notifications"),
                    ]
                ),
                CardContent(
                    children=[
                        Column(
                            gap=6,
                            children=[
                                # Email notifications
                                Row(
                                    justify="between",
                                    align="start",
                                    children=[
                                        Column(
                                            gap=1,
                                            children=[
                                                Text(
                                                    "Email Notifications", class_name="font-medium"
                                                ),
                                                Text(
                                                    "Receive emails about your account activity",
                                                    class_name="text-sm text-muted-foreground",
                                                ),
                                            ],
                                        ),
                                        Switch(
                                            checked=email_notifications,
                                            on_checked_change=ctx.callback(
                                                toggle_setting, key="email_notifications"
                                            ),
                                        ),
                                    ],
                                ),
                                Separator(),
                                # Push notifications
                                Row(
                                    justify="between",
                                    align="start",
                                    children=[
                                        Column(
                                            gap=1,
                                            children=[
                                                Text(
                                                    "Push Notifications", class_name="font-medium"
                                                ),
                                                Text(
                                                    "Receive push notifications on your devices",
                                                    class_name="text-sm text-muted-foreground",
                                                ),
                                            ],
                                        ),
                                        Switch(
                                            checked=push_notifications,
                                            on_checked_change=ctx.callback(
                                                toggle_setting, key="push_notifications"
                                            ),
                                        ),
                                    ],
                                ),
                                Separator(),
                                # Marketing emails
                                Row(
                                    justify="between",
                                    align="start",
                                    children=[
                                        Column(
                                            gap=1,
                                            children=[
                                                Text("Marketing Emails", class_name="font-medium"),
                                                Text(
                                                    "Receive emails about new products and features",
                                                    class_name="text-sm text-muted-foreground",
                                                ),
                                            ],
                                        ),
                                        Switch(
                                            checked=marketing_emails,
                                            on_checked_change=ctx.callback(
                                                toggle_setting, key="marketing_emails"
                                            ),
                                        ),
                                    ],
                                ),
                                Separator(),
                                # Weekly digest
                                Row(
                                    justify="between",
                                    align="start",
                                    children=[
                                        Column(
                                            gap=1,
                                            children=[
                                                Text("Weekly Digest", class_name="font-medium"),
                                                Text(
                                                    "Get a weekly summary of your activity",
                                                    class_name="text-sm text-muted-foreground",
                                                ),
                                            ],
                                        ),
                                        Switch(
                                            checked=weekly_digest,
                                            on_checked_change=ctx.callback(
                                                toggle_setting, key="weekly_digest"
                                            ),
                                        ),
                                    ],
                                ),
                                # Save button
                                Row(
                                    justify="end",
                                    class_name="mt-4",
                                    children=[
                                        Button(
                                            label="Save Preferences",
                                            on_click=ctx.callback(save_notifications),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

    elif active_section == "appearance":
        content = Card(
            children=[
                CardHeader(
                    children=[
                        CardTitle("Appearance"),
                        CardDescription("Customize the look and feel of the application"),
                    ]
                ),
                CardContent(
                    children=[
                        Column(
                            gap=6,
                            children=[
                                # Theme selection
                                Column(
                                    gap=3,
                                    children=[
                                        Label("Theme"),
                                        Row(
                                            gap=4,
                                            children=[
                                                Card(
                                                    class_name=f"cursor-pointer p-4 {'ring-2 ring-primary' if theme == 'light' else ''}",
                                                    children=[
                                                        Column(
                                                            gap=2,
                                                            align="center",
                                                            children=[
                                                                Container(
                                                                    class_name="w-16 h-12 bg-white border rounded",
                                                                ),
                                                                Text("Light", class_name="text-sm"),
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                                Card(
                                                    class_name=f"cursor-pointer p-4 {'ring-2 ring-primary' if theme == 'dark' else ''}",
                                                    children=[
                                                        Column(
                                                            gap=2,
                                                            align="center",
                                                            children=[
                                                                Container(
                                                                    class_name="w-16 h-12 bg-slate-900 border rounded",
                                                                ),
                                                                Text("Dark", class_name="text-sm"),
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                                Card(
                                                    class_name=f"cursor-pointer p-4 {'ring-2 ring-primary' if theme == 'system' else ''}",
                                                    children=[
                                                        Column(
                                                            gap=2,
                                                            align="center",
                                                            children=[
                                                                Container(
                                                                    class_name="w-16 h-12 bg-gradient-to-r from-white to-slate-900 border rounded",
                                                                ),
                                                                Text(
                                                                    "System", class_name="text-sm"
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                Separator(),
                                # Language selection
                                Column(
                                    gap=2,
                                    children=[
                                        Label("Language"),
                                        Select(
                                            value=language,
                                            options=[
                                                {"value": "en", "label": "English"},
                                                {"value": "es", "label": "Español"},
                                                {"value": "fr", "label": "Français"},
                                                {"value": "de", "label": "Deutsch"},
                                                {"value": "ja", "label": "日本語"},
                                            ],
                                        ),
                                    ],
                                ),
                                Separator(),
                                # Font size
                                Column(
                                    gap=2,
                                    children=[
                                        Label("Font Size"),
                                        Select(
                                            value=ctx.state.get("font_size", "medium"),
                                            options=[
                                                {"value": "small", "label": "Small"},
                                                {"value": "medium", "label": "Medium"},
                                                {"value": "large", "label": "Large"},
                                            ],
                                        ),
                                    ],
                                ),
                                # Save button
                                Row(
                                    justify="end",
                                    class_name="mt-4",
                                    children=[
                                        Button(
                                            label="Save Appearance",
                                            on_click=ctx.callback(save_appearance),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

    elif active_section == "security":
        content = Card(
            children=[
                CardHeader(
                    children=[
                        CardTitle("Security"),
                        CardDescription("Manage your account security settings"),
                    ]
                ),
                CardContent(
                    children=[
                        Column(
                            gap=6,
                            children=[
                                # Change password
                                Column(
                                    gap=4,
                                    children=[
                                        Text("Change Password", class_name="font-medium"),
                                        Column(
                                            gap=2,
                                            children=[
                                                Label("Current Password"),
                                                Input(
                                                    name="current_password",
                                                    type="password",
                                                    placeholder="••••••••",
                                                ),
                                            ],
                                        ),
                                        Column(
                                            gap=2,
                                            children=[
                                                Label("New Password"),
                                                Input(
                                                    name="new_password",
                                                    type="password",
                                                    placeholder="••••••••",
                                                ),
                                            ],
                                        ),
                                        Column(
                                            gap=2,
                                            children=[
                                                Label("Confirm New Password"),
                                                Input(
                                                    name="confirm_new_password",
                                                    type="password",
                                                    placeholder="••••••••",
                                                ),
                                            ],
                                        ),
                                        Button(label="Update Password", variant="outline"),
                                    ],
                                ),
                                Separator(),
                                # Two-factor auth
                                Row(
                                    justify="between",
                                    align="center",
                                    children=[
                                        Column(
                                            gap=1,
                                            children=[
                                                Row(
                                                    gap=2,
                                                    align="center",
                                                    children=[
                                                        Text(
                                                            "Two-Factor Authentication",
                                                            class_name="font-medium",
                                                        ),
                                                        Badge(
                                                            label="Recommended", variant="secondary"
                                                        ),
                                                    ],
                                                ),
                                                Text(
                                                    "Add an extra layer of security to your account",
                                                    class_name="text-sm text-muted-foreground",
                                                ),
                                            ],
                                        ),
                                        Button(label="Enable", variant="outline"),
                                    ],
                                ),
                                Separator(),
                                # Active sessions
                                Column(
                                    gap=4,
                                    children=[
                                        Text("Active Sessions", class_name="font-medium"),
                                        Card(
                                            class_name="p-4",
                                            children=[
                                                Row(
                                                    justify="between",
                                                    align="center",
                                                    children=[
                                                        Column(
                                                            gap=1,
                                                            children=[
                                                                Row(
                                                                    gap=2,
                                                                    align="center",
                                                                    children=[
                                                                        Text(
                                                                            "Windows • Chrome",
                                                                            class_name="font-medium",
                                                                        ),
                                                                        Badge(
                                                                            label="Current",
                                                                            variant="success",
                                                                        ),
                                                                    ],
                                                                ),
                                                                Text(
                                                                    "Last active: Now",
                                                                    class_name="text-xs text-muted-foreground",
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                        Card(
                                            class_name="p-4",
                                            children=[
                                                Row(
                                                    justify="between",
                                                    align="center",
                                                    children=[
                                                        Column(
                                                            gap=1,
                                                            children=[
                                                                Text(
                                                                    "iPhone • Safari",
                                                                    class_name="font-medium",
                                                                ),
                                                                Text(
                                                                    "Last active: 2 hours ago",
                                                                    class_name="text-xs text-muted-foreground",
                                                                ),
                                                            ],
                                                        ),
                                                        Button(
                                                            label="Revoke",
                                                            variant="ghost",
                                                            size="sm",
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

    elif active_section == "billing":
        content = Card(
            children=[
                CardHeader(
                    children=[
                        CardTitle("Billing"),
                        CardDescription("Manage your subscription and payment methods"),
                    ]
                ),
                CardContent(
                    children=[
                        Column(
                            gap=6,
                            children=[
                                # Current plan
                                Card(
                                    class_name="bg-muted/50 p-6",
                                    children=[
                                        Row(
                                            justify="between",
                                            align="center",
                                            children=[
                                                Column(
                                                    gap=1,
                                                    children=[
                                                        Row(
                                                            gap=2,
                                                            align="center",
                                                            children=[
                                                                Text(
                                                                    "Pro Plan",
                                                                    class_name="text-xl font-bold",
                                                                ),
                                                                Badge(
                                                                    label="Active",
                                                                    variant="success",
                                                                ),
                                                            ],
                                                        ),
                                                        Text(
                                                            "$29/month • Renews on Jan 15, 2025",
                                                            class_name="text-sm text-muted-foreground",
                                                        ),
                                                    ],
                                                ),
                                                Button(label="Manage Plan", variant="outline"),
                                            ],
                                        ),
                                    ],
                                ),
                                Separator(),
                                # Payment method
                                Column(
                                    gap=4,
                                    children=[
                                        Row(
                                            justify="between",
                                            align="center",
                                            children=[
                                                Text("Payment Method", class_name="font-medium"),
                                                Button(label="Add New", variant="ghost", size="sm"),
                                            ],
                                        ),
                                        Card(
                                            class_name="p-4",
                                            children=[
                                                Row(
                                                    justify="between",
                                                    align="center",
                                                    children=[
                                                        Row(
                                                            gap=3,
                                                            align="center",
                                                            children=[
                                                                Container(
                                                                    class_name="w-12 h-8 bg-blue-600 rounded flex items-center justify-center",
                                                                    children=[
                                                                        Text(
                                                                            "VISA",
                                                                            class_name="text-white text-xs font-bold",
                                                                        ),
                                                                    ],
                                                                ),
                                                                Column(
                                                                    gap=0,
                                                                    children=[
                                                                        Text(
                                                                            "•••• •••• •••• 4242",
                                                                            class_name="font-medium",
                                                                        ),
                                                                        Text(
                                                                            "Expires 12/25",
                                                                            class_name="text-xs text-muted-foreground",
                                                                        ),
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                        Badge(label="Default"),
                                                    ],
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                Separator(),
                                # Billing history
                                Column(
                                    gap=4,
                                    children=[
                                        Text("Billing History", class_name="font-medium"),
                                        Container(
                                            class_name="border rounded-md",
                                            children=[
                                                Row(
                                                    class_name="p-3 border-b",
                                                    justify="between",
                                                    children=[
                                                        Text("Dec 15, 2024"),
                                                        Text("$29.00"),
                                                        Badge(label="Paid", variant="success"),
                                                        Button(
                                                            label="Download",
                                                            variant="ghost",
                                                            size="sm",
                                                        ),
                                                    ],
                                                ),
                                                Row(
                                                    class_name="p-3 border-b",
                                                    justify="between",
                                                    children=[
                                                        Text("Nov 15, 2024"),
                                                        Text("$29.00"),
                                                        Badge(label="Paid", variant="success"),
                                                        Button(
                                                            label="Download",
                                                            variant="ghost",
                                                            size="sm",
                                                        ),
                                                    ],
                                                ),
                                                Row(
                                                    class_name="p-3",
                                                    justify="between",
                                                    children=[
                                                        Text("Oct 15, 2024"),
                                                        Text("$29.00"),
                                                        Badge(label="Paid", variant="success"),
                                                        Button(
                                                            label="Download",
                                                            variant="ghost",
                                                            size="sm",
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

    return Container(
        class_name="min-h-screen bg-background",
        children=[
            Row(
                children=[
                    # Sidebar
                    Container(
                        class_name="w-64 border-r min-h-screen p-4",
                        children=[
                            Column(
                                gap=6,
                                children=[
                                    Text("Settings", class_name="text-xl font-bold px-2"),
                                    Column(
                                        gap=1,
                                        children=[
                                            Button(
                                                label=item["label"],
                                                variant="default"
                                                if active_section == item["id"]
                                                else "ghost",
                                                class_name="w-full justify-start",
                                                on_click=ctx.callback(
                                                    change_section, section=item["id"]
                                                ),
                                            )
                                            for item in menu_items
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    # Main content
                    Container(
                        class_name="flex-1 p-8",
                        children=[
                            Container(
                                class_name="max-w-2xl",
                                children=[content],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


# Create FastAPI app and include Refast
app = FastAPI()
app.include_router(ui.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
