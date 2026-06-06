import uvicorn
from fastapi import FastAPI

from refast import Context, RefastApp
from refast.components import (
    Button,
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
    Checkbox,
    Column,
    Container,
    Grid,
    Heading,
    Input,
    Row,
    Text,
)

ui = RefastApp(title="Refast Desktop Notifications Showcase")


async def handle_click(ctx: Context):
    """Fired when the desktop notification is clicked."""
    await ctx.show_toast("Notification Clicked! Window focused.", variant="success")
    # You could also perform navigation or other actions here
    # e.g., await ctx.load("/details")


async def handle_close(ctx: Context):
    """Fired when the desktop notification is dismissed."""
    await ctx.show_toast("Notification Closed/Dismissed", variant="info")


async def handle_permission_granted(ctx: Context):
    """Fired when notification permission is granted."""
    await ctx.show_toast("Notification Permission: GRANTED", variant="success")
    await ctx.update_text("permission-status", "Permission Status: Granted")
    await ctx.update_props(
        "permission-status-badge",
        {
            "class_name": "text-xs px-2.5 py-0.5 rounded-full font-semibold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30"
        },
    )


async def handle_permission_denied(ctx: Context):
    """Fired when notification permission is denied."""
    await ctx.show_toast("Notification Permission: DENIED", variant="error")
    await ctx.update_text("permission-status", "Permission Status: Denied/Blocked")
    await ctx.update_props(
        "permission-status-badge",
        {
            "class_name": "text-xs px-2.5 py-0.5 rounded-full font-semibold bg-rose-500/20 text-rose-400 border border-rose-500/30"
        },
    )


async def trigger_notification(
    ctx: Context,
    notif_title: str = "Refast Native Alert",
    notif_body: str = "This is a native system notification sent from the backend!",
    notif_tag: str = "refast-alert-group",
    notif_silent: bool = False,
    notif_require_interaction: bool = False,
):
    """Trigger the native desktop notification using input values."""
    # Retrieve form values from local storage/props if they aren't directly passed or are empty
    title_val = notif_title or "Refast Alert"
    body_val = notif_body or "This is a native system notification sent from the backend!"
    tag_val = notif_tag or None

    await ctx.show_toast(
        "Sending notification request...", variant="loading", toast_id="notify-req"
    )

    await ctx.show_desktop_notification(
        title=title_val,
        body=body_val,
        icon="https://refast.dev/logo.png",  # Example placeholder icon
        tag=tag_val,
        silent=notif_silent,
        require_interaction=notif_require_interaction,
        on_click=ctx.callback(handle_click),
        on_close=ctx.callback(handle_close),
        on_permission_granted=ctx.callback(handle_permission_granted),
        on_permission_denied=ctx.callback(handle_permission_denied),
    )

    await ctx.show_toast("Notification request sent!", variant="success", toast_id="notify-req")


@ui.page("/")
def notification_demo_page(ctx: Context):
    # Initialize default inputs in store
    ctx.store.local["notif_title"] = ctx.store.local.get("notif_title", "Refast Native Alert")
    ctx.store.local["notif_body"] = ctx.store.local.get(
        "notif_body", "Backend-triggered system notification!"
    )
    ctx.store.local["notif_tag"] = ctx.store.local.get("notif_tag", "refast-alert-group")
    ctx.store.local["notif_silent"] = ctx.store.local.get("notif_silent", False)
    ctx.store.local["notif_require_interaction"] = ctx.store.local.get("notif_require_interaction", False)

    header = Card(
        class_name="mb-6 bg-slate-900 border-slate-800 text-slate-100",
        children=[
            CardContent(
                class_name="py-4 px-6 flex flex-row justify-between items-center",
                children=[
                    Column(
                        gap=1,
                        children=[
                            Heading(
                                "Desktop Notifications",
                                level=2,
                                class_name="font-extrabold text-xl text-purple-400",
                            ),
                            Text(
                                "Demonstrates native system-level desktop notifications with interactive Python callbacks",
                                class_name="text-xs text-slate-400",
                            ),
                        ],
                    ),
                ],
            )
        ],
    )

    control_card = Card(
        class_name="bg-slate-950 border-slate-800 text-slate-100 shadow-xl",
        children=[
            CardHeader(
                children=[
                    CardTitle(
                        "Notification Settings", class_name="text-lg font-bold text-slate-200"
                    ),
                    CardDescription(
                        "Customize the native desktop notification payload below.",
                        class_name="text-xs text-slate-400",
                    ),
                ]
            ),
            CardContent(
                children=[
                    Column(
                        gap=4,
                        children=[
                            # Title input
                            Column(
                                gap=2,
                                children=[
                                    Text(
                                        "Notification Title",
                                        class_name="text-sm font-semibold text-slate-300",
                                    ),
                                    Input(
                                        placeholder="Enter notification title...",
                                        value=ctx.store.local["notif_title"],
                                        on_change=ctx.save_prop("notif_title"),
                                        class_name="bg-slate-900 border-slate-800 text-slate-200 placeholder:text-slate-600 focus:border-purple-500",
                                    ),
                                ],
                            ),
                            # Body input
                            Column(
                                gap=2,
                                children=[
                                    Text(
                                        "Notification Message (Body)",
                                        class_name="text-sm font-semibold text-slate-300",
                                    ),
                                    Input(
                                        placeholder="Enter notification body/message...",
                                        value=ctx.store.local["notif_body"],
                                        on_change=ctx.save_prop("notif_body"),
                                        class_name="bg-slate-900 border-slate-800 text-slate-200 placeholder:text-slate-600 focus:border-purple-500",
                                    ),
                                ],
                            ),
                            # Tag input (de-duplication)
                            Column(
                                gap=2,
                                children=[
                                    Text(
                                        "Deduplication Tag",
                                        class_name="text-sm font-semibold text-slate-300",
                                    ),
                                    Text(
                                        "Notifications with the same tag will replace each other instead of piling up.",
                                        class_name="text-[11px] text-slate-500",
                                    ),
                                    Input(
                                        placeholder="Enter unique tag...",
                                        value=ctx.store.local["notif_tag"],
                                        on_change=ctx.save_prop("notif_tag"),
                                        class_name="bg-slate-900 border-slate-800 text-slate-200 placeholder:text-slate-600 focus:border-purple-500",
                                    ),
                                ],
                            ),
                            # Configuration checkboxes
                            Row(
                                gap=6,
                                children=[
                                    Row(
                                        gap=2,
                                        align="center",
                                        children=[
                                            Checkbox(
                                                id="chk-silent",
                                                checked=ctx.store.local["notif_silent"],
                                                on_change=ctx.save_prop("notif_silent"),
                                            ),
                                            Text(
                                                "Silent (No System Sound)",
                                                class_name="text-sm text-slate-300",
                                            ),
                                        ],
                                    ),
                                    Row(
                                        gap=2,
                                        align="center",
                                        children=[
                                            Checkbox(
                                                id="chk-interact",
                                                checked=ctx.store.local["notif_req_interact"],
                                                on_change=ctx.save_prop("notif_req_interact"),
                                            ),
                                            Text(
                                                "Require Interaction",
                                                class_name="text-sm text-slate-300",
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    )
                ]
            ),
        ],
    )

    info_card = Card(
        class_name="bg-slate-950 border-slate-800 text-slate-100 shadow-xl",
        children=[
            CardHeader(
                children=[
                    CardTitle(
                        "Callback Logging & Status", class_name="text-lg font-bold text-slate-200"
                    ),
                    CardDescription(
                        "Real-time permission and interaction state.",
                        class_name="text-xs text-slate-400",
                    ),
                ]
            ),
            CardContent(
                children=[
                    Column(
                        gap=4,
                        children=[
                            Row(
                                align="center",
                                gap=3,
                                children=[
                                    Text(
                                        "Current State:",
                                        class_name="text-sm font-semibold text-slate-400",
                                    ),
                                    Container(
                                        id="permission-status-badge",
                                        class_name="text-xs px-2.5 py-0.5 rounded-full font-semibold bg-slate-800 text-slate-400 border border-slate-700",
                                        children=[
                                            Text(
                                                "Unknown (Awaiting request)", id="permission-status"
                                            )
                                        ],
                                    ),
                                ],
                            ),
                            Text(
                                "Note: The browser/webview will prompt for permission when the first notification is sent. If you deny it, notifications are silently blocked by the operating system.",
                                class_name="text-xs text-slate-400 leading-relaxed",
                            ),
                            Button(
                                "Send Native Notification",
                                variant="default",
                                on_click=ctx.callback(
                                    trigger_notification,
                                    props=[
                                        "notif_title",
                                        "notif_body",
                                        "notif_tag",
                                        "notif_silent",
                                        "notif_req_interact",
                                    ],
                                ),
                                class_name="w-full bg-purple-600 hover:bg-purple-500 text-white font-bold py-2 rounded-lg transition-all shadow-lg shadow-purple-900/30",
                            ),
                        ],
                    )
                ]
            ),
        ],
    )

    return Container(
        class_name="min-h-screen p-6 bg-slate-950 flex flex-col",
        children=[
            header,
            Grid(
                columns=2,
                gap=6,
                class_name="flex-grow",
                children=[
                    control_card,
                    info_card,
                ],
            ),
        ],
    )


app = FastAPI()
app.include_router(ui.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
