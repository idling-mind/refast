"""Pydantic models for incoming WebSocket messages."""

from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter
from pydantic.alias_generators import to_camel


class BaseMessage(BaseModel):
    """Base model for WebSocket messages with camelCase conversion."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class CallbackMessage(BaseMessage):
    """Payload for callback invocation."""

    type: Literal["callback"]
    callback_id: str
    data: dict[str, Any] = Field(default_factory=dict)
    event_data: Any = Field(default_factory=dict)


class StoreInitMessage(BaseMessage):
    """Payload for store initialization."""

    type: Literal["store_init"]
    data: dict[str, Any] = Field(default_factory=dict)
    path: str = "/"


class NavigateMessage(BaseMessage):
    """Payload for navigation."""

    type: Literal["navigate"]
    path: str = "/"


class EventMessage(BaseMessage):
    """Payload for custom event."""

    type: Literal["event"]
    event_type: str
    data: dict[str, Any] = Field(default_factory=dict)


class StoreSyncMessage(BaseMessage):
    """Payload for store synchronization."""

    type: Literal["store_sync"]
    data: dict[str, Any] = Field(default_factory=dict)


ClientMessage = Annotated[
    CallbackMessage | StoreInitMessage | NavigateMessage | EventMessage | StoreSyncMessage,
    Field(discriminator="type"),
]

client_message_adapter = TypeAdapter(ClientMessage)
