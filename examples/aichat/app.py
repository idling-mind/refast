from turtle import st
from operator import le
from fastapi import FastAPI
from refast import Context, RefastApp, components as rc

ui = RefastApp(title="AI Chat Example")

dummy_chats = [
    {"title": "Chat with AI", "tags": ["AI", "Chat"], "timestamp": "2h ago"},
    {"title": "Project Brainstorming", "tags": ["Project", "Ideas"], "timestamp": "1d ago"},
    {"title": "Code Review", "tags": ["Code", "Review"], "timestamp": "3d ago"},
]


def left_panel(chats: list[dict[str, str]] = dummy_chats):
    return rc.Column(
        class_name="h-full",
        children=[
            rc.Row(
                class_name="border-b p-2 py-4",
                children=[
                    rc.Button(
                        label="New Chat",
                        class_name="w-full rounded-full",
                    ),
                ],
            ),
            rc.Row(
                class_name="border-b p-2 py-4",
                children=[
                    rc.Container(
                        class_name="flex-1",
                        children=[
                            rc.Input(
                                placeholder="Search chats...",
                                class_name="w-full",
                            ),
                        ],
                    ),
                ],
            ),
            rc.Row(
                class_name="flex-1 overflow-hidden",
                children=[
                rc.Column(
                    class_name="h-full w-full overflow-y-auto",
                    children=[
                        chat_list_item(**chat) for chat in chats
                    ],
                    align="stretch",
                    justify="start",
                )
            ]),
            rc.Row(
                class_name="border-t p-2",
                style={"height": "40px"},
                children=[
                    rc.IconButton(icon="settings", aria_label="Settings"),
                    rc.ThemeSwitcher(mode="dropdown", parent_style={"border": "none", "background": "transparent"}),
                ],
                gap=2,
            ),
        ],
        align="stretch",
        gap=0,
    )

def main_panel():
    return rc.Column(
        class_name="h-full",
        children=[
            rc.Row(
                class_name="border-b p-2",
                children=[
                    rc.IconButton(
                        icon="menu",
                    ),
                    rc.Text("Chat with AI", class_name="font-semibold"),
                    rc.Text("4 Messages, 2 Artifacts", class_name="text-sm text-gray-500"),
                    rc.Container(class_name="flex-1"),
                    rc.ConnectionStatus(
                        position="inline",
                        children_connected=[rc.Icon("wifi", color="green")],
                        children_disconnected=[rc.Icon("wifi-off", color="red")],
                    ),
                ],
                align="center",
            ),
            rc.Row(class_name="flex-1", children=["Chat history"]),
            rc.Row(
                class_name="border-t p-2",
                style={"height": "40px"},
                children=[
                    rc.Card(
                        class_name="flex-1 p-2",
                        style={"background-color": "rgba(128, 128, 178, 0.05)"},
                        children = [
                            rc.Column(
                                children=[
                                    rc.Textarea(
                                        placeholder="Type your message...",
                                        class_name="w-full bg-transparent",
                                        style={"border": "none", "resize": "none", "outline": "none"},
                                    ),
                                    rc.Row(
                                        children=[
                                            rc.Combobox(
                                                label="Select Agent",
                                                options=[
                                                    {
                                                        "value": "react",
                                                        "label": "React",
                                                        "description": "Component-first UI library",
                                                        "icon": "layers",
                                                        "color": "#61DAFB",
                                                        "search_text": "jsx hooks frontend",
                                                    },
                                                    {
                                                        "value": "vue",
                                                        "label": "Vue",
                                                        "description": "Progressive framework",
                                                        "icon": "code",
                                                        "color": "#42B883",
                                                        "search_text": "sfc composition api",
                                                    },
                                                    {
                                                        "value": "angular",
                                                        "label": "Angular",
                                                        "description": "Full-featured application framework",
                                                        "icon": "shield",
                                                        "color": "#DD0031",
                                                    },
                                                    {
                                                        "value": "svelte",
                                                        "label": "Svelte",
                                                        "description": "Compile-time reactive UI",
                                                        "icon": "zap",
                                                        "color": "#FF3E00",
                                                        "disabled": True,
                                                    },
                                                ],
                                                parent_style={"width": "200px"},
                                                placeholder="Select agent"
                                            ),
                                            rc.Tooltip(
                                                children=rc.IconButton(icon="upload", aria_label="Attach file", class_name="rounded-full"),
                                                content="Upload file",
                                            ),
                                            rc.Tooltip(
                                                children=rc.IconButton(icon="layout-dashboard", aria_label="Select tools", class_name="rounded-full"),
                                                content="Select tools",
                                            ),
                                            rc.Container(class_name="flex-1"),
                                            rc.Tooltip(
                                                children=rc.IconButton(icon="send", aria_label="Send message", class_name="rounded-full", variant="default"),
                                                content="Send message",
                                            ),
                                        ]
                                    ),
                                ]
                            )
                        ]
                    )
                ],
                gap=2,
            ),
        ],
        align="stretch",
    )

def chat_list_item(title: str, tags: list[str], timestamp: str):
    return rc.Row(
        class_name="p-2 hover:bg-muted cursor-pointer w-full",
        children=[
            rc.Column(children=rc.Icon("message-square"), class_name="m-2"),
            rc.Column(
                children=[
                    rc.Text(title, class_name="font-medium"),
                    rc.Row(
                        children=[
                            rc.Badge(tag, variant="secondary") for tag in tags
                        ],
                        gap=1,
                    ),
                    rc.Text(timestamp, class_name="text-xs text-gray-400"),
                ],
                align="stretch",
                justify="start",
            ),
        ],
    )

@ui.page("/")
def home(ctx: Context):
    return rc.Container(
        class_name="h-screen",
        children=[
            rc.ResizablePanelGroup(
                direction="horizontal",
                children=[
                    rc.ResizablePanel(
                        children=[left_panel()],
                        min_size=10,
                        max_size=40,
                        default_size=20,
                    ),
                    rc.ResizableHandle(with_handle=True),
                    rc.ResizablePanel(
                        children=[main_panel()],
                        default_size=40,
                    ),
                    rc.ResizableHandle(with_handle=True),
                    rc.ResizablePanel(
                        children=[rc.Text("Artifacts", class_name="text-gray-500 italic")],
                        default_size=20,
                    ),
                ],
            )
        ]
    )

app = FastAPI(title="AI Chat Example", debug=True)
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)