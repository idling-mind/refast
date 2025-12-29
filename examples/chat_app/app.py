"""Chat App Example - Real-time Chat Application.

This example demonstrates:
- Real-time WebSocket communication
- Broadcasting messages to all connected clients
- User session management
- Message history within session
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List
import uuid

from fastapi import FastAPI

from refast import RefastApp, Context
from refast.components import (
    Container,
    Column,
    Row,
    Text,
    Button,
    Card,
    CardHeader,
    CardContent,
    CardTitle,
    Input,
    Badge,
    Avatar,
)


@dataclass
class Message:
    """A chat message."""
    id: str
    username: str
    text: str
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "username": self.username,
            "text": self.text,
            "timestamp": self.timestamp.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Message":
        """Create from dictionary."""
        return cls(
            id=data["id"],
            username=data["username"],
            text=data["text"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )


# Global message store (in production, use Redis or database)
MESSAGES: list[Message] = []
MAX_MESSAGES = 50


# Create the Refast app
ui = RefastApp(title="Chat App")


def get_username(ctx: Context) -> str:
    """Get or generate username."""
    username = ctx.state.get("username", "")
    if not username:
        username = f"User_{uuid.uuid4().hex[:6]}"
        ctx.state.set("username", username)
    return username


async def set_username(ctx: Context, username: str = ""):
    """Set the username."""
    if username.strip():
        ctx.state.set("username", username.strip())


async def update_message_text(ctx: Context, value: str):
    """Update message text state."""
    ctx.state.set("message_text", value)
    print("Updated message text:", value)


async def send_message(ctx: Context):
    """Send a new message."""
    text = ctx.state.get("message_text", "")
    if not text.strip():
        return
    
    username = get_username(ctx)
    message = Message(
        id=str(uuid.uuid4()),
        username=username,
        text=text.strip(),
    )
    
    MESSAGES.append(message)
    
    # Keep only last N messages
    while len(MESSAGES) > MAX_MESSAGES:
        MESSAGES.pop(0)
    
    # Clear input
    ctx.state.set("message_text", "")
    print(f"Sent message from {username}: {text.strip()}")
    print(f"All messages: {[m.to_dict() for m in MESSAGES]}")
    
    # Use replace() for efficient partial update - only update the messages list
    await ctx.replace("messages-list", render_messages_list(MESSAGES, username))
    
    # TODO: Broadcast to all connected clients
    # await ctx.broadcast("chat:message", message.to_dict())


def render_message(message: Message, current_user: str):
    """Render a single message."""
    is_own = message.username == current_user
    
    return Row(
        id=f"msg-{message.id}",
        class_name=f"{'flex-row-reverse' if is_own else ''}",
        gap=2,
        children=[
            Avatar(
                name=message.username,
                size="sm",
            ),
            Container(
                class_name=f"max-w-xs p-3 rounded-lg {'bg-blue-500 text-blue-200' if is_own else 'bg-gray-100'}",
                children=[
                    Column(
                        gap=1,
                        children=[
                            Text(
                                message.username,
                                class_name=f"text-xs font-semibold {'text-blue-100' if is_own else 'text-gray-500'}",
                            ) if not is_own else Container(),
                            Text(message.text),
                            Text(
                                message.timestamp.strftime("%H:%M"),
                                class_name=f"text-xs {'text-blue-200' if is_own else 'text-gray-400'}",
                            ),
                        ],
                    )
                ],
            ),
        ],
    )


def render_messages_list(messages: list[Message], current_user: str):
    """Render the messages list component."""
    return Column(
        id="messages-list",
        gap=3,
        class_name="py-4",
        children=[
            render_message(msg, current_user)
            for msg in messages
        ] if messages else [
            Container(
                class_name="text-center py-16",
                children=[
                    Text(
                        "No messages yet",
                        class_name="text-gray-400",
                    ),
                    Text(
                        "Start the conversation!",
                        class_name="text-gray-400 text-sm",
                    ),
                ],
            )
        ],
    )


@ui.page("/")
def chat(ctx: Context):
    """Main chat page."""
    username = get_username(ctx)
    
    return Container(
        id="main-container",
        class_name="max-w-2xl mx-auto mt-6 px-4 h-screen flex flex-col",
        children=[
            Card(
                id="chat-card",
                class_name="flex-1 flex flex-col",
                children=[
                    # Header
                    CardHeader(
                        class_name="border-b",
                        children=[
                            Row(
                                justify="between",
                                align="center",
                                children=[
                                    CardTitle("Chat Room"),
                                    Row(
                                        gap=2,
                                        align="center",
                                        children=[
                                            Text(
                                                "Logged in as:",
                                                class_name="text-sm text-gray-500",
                                            ),
                                            Badge(username, variant="default"),
                                        ],
                                    ),
                                ],
                            )
                        ]
                    ),
                    # Messages area
                    CardContent(
                        class_name="flex-1 overflow-y-auto",
                        children=[
                            render_messages_list(MESSAGES, username)
                        ]
                    ),
                    # Input area
                    Container(
                        class_name="p-4 border-t",
                        children=[
                            Row(
                                gap=2,
                                children=[
                                    Container(
                                        class_name="flex-1",
                                        children=[
                                            Input(
                                                id="message-input",
                                                name="message",
                                                placeholder="Type a message...",
                                                value=ctx.state.get("message_text", ""),
                                                on_change=ctx.callback(update_message_text),
                                            )
                                        ],
                                    ),
                                    Button(
                                        "Send",
                                        id="send-btn",
                                        variant="primary",
                                        on_click=ctx.callback(send_message),
                                    ),
                                ],
                            )
                        ],
                    ),
                ]
            )
        ],
    )


async def update_draft_username(ctx: Context, value: str):
    """Update draft username."""
    ctx.state.set("draft_username", value)


async def save_username(ctx: Context):
    """Save the username from draft."""
    draft = ctx.state.get("draft_username")
    if draft:
        await set_username(ctx, draft)


@ui.page("/settings")
def settings(ctx: Context):
    """User settings page."""
    username = get_username(ctx)
    draft_username = ctx.state.get("draft_username", username)
    
    return Container(
        id="settings-container",
        class_name="max-w-md mx-auto mt-10 px-4",
        children=[
            Card(
                children=[
                    CardHeader(
                        children=[
                            CardTitle("Settings"),
                        ]
                    ),
                    CardContent(
                        children=[
                            Column(
                                gap=4,
                                children=[
                                    Column(
                                        gap=2,
                                        children=[
                                            Text(
                                                "Username",
                                                class_name="text-sm font-medium",
                                            ),
                                            Row(
                                                gap=2,
                                                children=[
                                                    Container(
                                                        class_name="flex-1",
                                                        children=[
                                                            Input(
                                                                id="username-input",
                                                                placeholder="Enter username",
                                                                value=draft_username,
                                                                on_change=ctx.callback(update_draft_username),
                                                            )
                                                        ],
                                                    ),
                                                    Button(
                                                        "Save",
                                                        variant="primary",
                                                        on_click=ctx.callback(save_username),
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                    Row(
                                        children=[
                                            Button(
                                                "← Back to Chat",
                                                variant="ghost",
                                                # TODO: Navigation
                                            ),
                                        ],
                                    ),
                                ],
                            )
                        ]
                    ),
                ]
            )
        ],
    )


# Create the FastAPI app and mount Refast
app = FastAPI(title="Refast Chat Example")
app.include_router(ui.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
